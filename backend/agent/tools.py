from langchain_core.tools import tool
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
import json

@tool
def search_the_web(query: str, max_results: int = 5) -> str:
    """Searches the web using DuckDuckGo and returns JSON results with title, link, and snippet."""
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append(r)
        return json.dumps(results)
    except Exception as e:
        return f"Error performing search: {e}"

@tool
def scrape_webpage(url: str) -> str:
    """Scrapes the text content from a given URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
            
        text = soup.get_text(separator=' ', strip=True)
        return text[:8000] # Limiting size to avoid context length overflow
    except Exception as e:
        return f"Error scraping page {url}: {e}"

tools = [search_the_web, scrape_webpage]
