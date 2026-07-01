from langchain_core.tools import tool
from vectorstore import vector_store
from rss_news import get_articles
from extract import extract_article

@tool
def search_news_database(query: str) -> str:
    """Search the existing vector DB of already-ingested AI news articles."""
    results = vector_store.similarity_search(query=query, k=8)
    if not results:
        return "No relevant articles found in the database."
    return "\n\n---\n\n".join(
        f"Source URL: {doc.metadata.get('URL')}\nContent: {doc.page_content}"
        for doc in results
    )
  
@tool
def get_latest_headlines() -> str:
    """Pull the latest headlines directly from RSS feeds (bypassing the vector DB), useful if the user wants something more recent than what's stored."""
    articles = get_articles(limit_per_feed=5)
    return "\n".join(f"- {a['title']} ({a['url']})" for a in articles)
