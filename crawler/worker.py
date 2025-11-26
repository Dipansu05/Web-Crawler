# crawler/worker.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

DEFAULT_HEADERS = {
    "User-Agent": "WebCrawler/1.0 (+https://github.com/Dipansu05)"
}

def fetch(url):
    r = requests.get(url, headers=DEFAULT_HEADERS, timeout=8)
    r.raise_for_status()
    return r.text

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

