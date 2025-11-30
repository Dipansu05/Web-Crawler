# crawler/worker.py
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from utils.logger import info, warn, error

DEFAULT_HEADERS = {
    "User-Agent": "WebCrawler/1.0 (+https://github.com/Dipansu05)"
}

def fetch(url, retries=3, backoff=1.5):
    """Fetch page with retry & backoff."""
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=8)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            warn(f"Fetch failed (attempt {attempt}): {url} ({e})")
            if attempt == retries:
                error(f"Giving up on: {url}")
                return None
            time.sleep(backoff * attempt)





def parse_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")

    # title
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    else:
        title = ""

    # meta tags
    metas = {}
    for m in soup.find_all("meta"):
        if m.get("name"):
            metas[m.get("name")] = m.get("content", "")
        if m.get("property"):
            metas[m.get("property")] = m.get("content", "")

    # links
    links = set()
    for a in soup.find_all("a", href=True):
        link = urljoin(base_url, a["href"])
        parsed = urlparse(link)
        if parsed.scheme in ("http", "https"):
            links.add(link.split("#")[0])

    return title, metas, links

