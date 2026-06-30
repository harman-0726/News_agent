import feedparser
import requests

RSS_FEEDS = [
    "https://venturebeat.com/category/ai/feed/",
    "https://www.marktechpost.com/feed/",
    "https://blog.google/technology/ai/rss/",
    "https://syncedreview.com/feed/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}


def get_articles(limit_per_feed=8):
    articles = []
    seen_urls = set()

    for feed_url in RSS_FEEDS:
        feed = None
        for attempt in range(2):
            try:
                resp = requests.get(feed_url, headers=HEADERS, timeout=15)
                resp.raise_for_status()
                feed = feedparser.parse(resp.content)
                if feed.entries:
                    break
                print(f"⚠️ Attempt {attempt + 1}: no entries from {feed_url} (bozo={feed.bozo})")
            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} error reading {feed_url}: {e}")
                feed = None

        if not feed or not feed.entries:
            print(f"❌ Failed to load: {feed_url}")
            continue

        try:
            for entry in feed.entries[:limit_per_feed]:

                url = entry.get("link")

                if not url or url in seen_urls:
                    continue

                seen_urls.add(url)

                articles.append({
                    "title": entry.get("title", "No Title"),
                    "url": url,
                    "published": entry.get("published", "Unknown")
                })

        except Exception as e:
            print(f"Error reading {feed_url}: {e}")

    return articles
