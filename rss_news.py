import feedparser

RSS_FEEDS = [
    "https://www.artificialintelligence-news.com/feed/",
    "https://www.marktechpost.com/feed/",
    "https://openai.com/news/rss.xml",
]


def get_articles(limit_per_feed=5):
    articles = []
    seen_urls = set()

    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)

            # Skip invalid feeds
            if feed.bozo:
                print(f"❌ Failed to load: {feed_url}")
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


