import os
import requests

WHATSAPP_TOKEN = os.environ["WHATSAPP_TOKEN"]
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]
API_VERSION = "v22.0"


def send_whatsapp_text(to: str, text: str):
    """Send a plain text WhatsApp message. `to` = recipient phone number
    in international format without '+' (e.g. '919876543210')."""
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)] or [text]

    for chunk in chunks:
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": chunk},
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=20)
        print(f"WhatsApp API response [{resp.status_code}] to {to}: {resp.text}")

def send_whatsapp_document(to: str, file_path: str, caption: str = ""):
    """Optional: upload + send a PDF document instead of/alongside text."""
    upload_url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/media"
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/pdf")}
        data = {"messaging_product": "whatsapp", "type": "application/pdf"}
        resp = requests.post(upload_url, headers=headers, files=files, data=data, timeout=30)

    media_id = resp.json().get("id")
    if not media_id:
        print(f"Media upload failed: {resp.text}")
        return

    send_url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "document",
        "document": {"id": media_id, "caption": caption, "filename": "ai_news_digest.pdf"},
    }
    # send the document message
    resp = requests.post(send_url, headers=headers, json=payload, timeout=20)
    print(f"WhatsApp API response [{resp.status_code}] to {to}: {resp.text}")
    if resp.status_code >= 400:
        print(f"WhatsApp send failed: {resp.status_code} {resp.text}")