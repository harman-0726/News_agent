import os
from contextlib import asynccontextmanager
import logging
logging.basicConfig(level=logging.INFO)
from fastapi import FastAPI, Request, Response
from apscheduler.schedulers.background import BackgroundScheduler
import pytz
from dotenv import load_dotenv

from rag import ingest_daily_news, run_daily_digest, agentic_answer
from Whatsapp import send_whatsapp_text

load_dotenv()

VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]          # you choose this, set it in Meta dashboard too
OWNER_PHONE = os.environ["OWNER_PHONE"]            # your own number, to receive the daily digest
DIGEST_HOUR = int(os.environ.get("DIGEST_HOUR", 19))  # 24h format, server timezone
DIGEST_MINUTE = int(os.environ.get("DIGEST_MINUTE", 0))  # 24h format, server timezone

def send_whatsapp_message(recipient: str, content):
    if not isinstance(content, str):
        content = str(content)
    send_whatsapp_text(recipient, content)

def scheduled_job():
    print("Running scheduled job: ingest + digest")
    ingest_daily_news(limit_per_feed=10)
    digest = run_daily_digest()
    send_whatsapp_message(OWNER_PHONE, digest)


scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(scheduled_job, "cron", hour=DIGEST_HOUR, minute=DIGEST_MINUTE, timezone=pytz.timezone("Asia/Kolkata"))
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/webhook")
def verify_webhook(request: Request):
    """Meta calls this once when you set up the webhook in the dashboard."""
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return Response(content=params.get("hub.challenge"), media_type="text/plain")
    return Response(content="Verification failed", status_code=403)


@app.post("/webhook")
async def receive_message(request: Request):
    """Meta calls this every time a user sends your WhatsApp number a message."""
    body = await request.json()

    try:
        entry = body["entry"][0]["changes"][0]["value"]
        messages = entry.get("messages")
        if not messages:
            return {"status": "ignored"}  # e.g. delivery/read receipts

        message = messages[0]
        sender = message["from"]
        user_text = message.get("text", {}).get("body", "")

        if not user_text:
            send_whatsapp_text(sender, "I can currently only understand text messages.")
            return {"status": "ok"}

        if user_text.strip().lower() in ("digest", "news", "today"):
            reply = run_daily_digest()
        else:
            reply = agentic_answer(user_text)

        send_whatsapp_message(sender, reply)

    except (KeyError, IndexError) as e:
        print(f"Webhook parse issue (likely a non-message event): {e}")

    return {"status": "ok"}


@app.get("/trigger-digest")
def manual_trigger():
    """Manual endpoint to test the daily job without waiting for the scheduler."""
    scheduled_job()
    return {"status": "digest sent"}
