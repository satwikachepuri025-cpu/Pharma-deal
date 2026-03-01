import feedparser
from app.config import MAX_ARTICLES
from app.logger import log_info

RSS_FEEDS = [
    "https://www.biopharmadive.com/feeds/news/",
    "https://www.fiercepharma.com/rss/xml",
    "https://www.pharmatimes.com/rss/news"
]


def fetch_articles():
    articles = []
    seen_urls = set()

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:

            link = entry.link

            if link in seen_urls:
                continue

            seen_urls.add(link)

            articles.append({
                "title": entry.title,
                "link": link,
                "summary": getattr(entry, "summary", "")
            })

            if len(articles) >= MAX_ARTICLES:
                break

        if len(articles) >= MAX_ARTICLES:
            break

    log_info(f"Fetched {len(articles)} articles from direct RSS feeds.")
    return articles