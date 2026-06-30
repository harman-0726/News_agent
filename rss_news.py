import feedparser
import requests

RSS_FEEDS = [
    "https://venturebeat.com/category/ai/feed/",
    "https://www.marktechpost.com/feed/",
    "https://openai.com/news/rss.xml",
    "https://blog.google/technology/ai/rss/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
}


def get_articles(limit_per_feed=7):
    articles = []
    seen_urls = set()

    for feed_url in RSS_FEEDS:
        try:
            # Fetch ourselves with browser-like headers; feedparser's own
            # fetcher gets blocked by some hosts (datacenter IP / no UA).
            resp = requests.get(feed_url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)

            # bozo just means "not perfectly well-formed XML" — many real
            # feeds set this even though entries parse fine. Only skip if
            # there are genuinely no entries.
            if not feed.entries:
                print(f"❌ No entries parsed from: {feed_url} (bozo={feed.bozo})")
                continue

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
