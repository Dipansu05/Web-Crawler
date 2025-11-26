import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor


class Crawler:
    def __init__(self, seeds, max_workers=5, max_pages=50, max_depth=2):
        self.seeds = seeds
        self.max_workers = max_workers
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited = set()
        self.results = []

    def fetch(self, url):
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            return r.text
        except Exception:
            return None

    def parse(self, html, base_url):
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""


        links = []
        for a in soup.find_all("a", href=True):
            link = urljoin(base_url, a['href'])
            links.append(link)

        return title, links

    def crawl_page(self, url, depth):
        if len(self.visited) >= self.max_pages:
            return

        if url in self.visited or depth > self.max_depth:
            return

        self.visited.add(url)

        html = self.fetch(url)
        if not html:
            return

        title, links = self.parse(html, url)
        print(f"[Crawled] {url} -> {title}")

        self.results.append({"url": url, "title": title})

        return [(link, depth + 1) for link in links]

    def start(self):
        queue = [(url, 0) for url in self.seeds]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            while queue and len(self.visited) < self.max_pages:
                url, depth = queue.pop(0)
                future = executor.submit(self.crawl_page, url, depth)
                next_links = future.result()
                if next_links:
                    queue.extend(next_links)

