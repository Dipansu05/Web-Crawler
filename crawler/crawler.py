# crawler/crawler.py
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty
from urllib.parse import urlparse

from crawler.worker import fetch, parse_html
from crawler.robots import RobotsChecker
from utils.db import CrawlerDB
from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    """Remove fragments, normalize scheme/host."""
    parsed = urlparse(url)
    clean = parsed._replace(fragment="")
    return urlunparse(clean)


class Crawler:
    def __init__(self, seeds, max_workers=8, max_pages=200, max_depth=2, ignore_robots=False):
        self.seeds = seeds
        self.max_workers = max_workers
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.ignore_robots = ignore_robots

        self.visited = set()
        self.queue = Queue()

        self.db = CrawlerDB("crawler.db")
        self.robots = RobotsChecker()

        # Allowed domains
        self.allowed_domains = {self.get_domain(url) for url in seeds}

    def get_domain(self, url):
        return urlparse(url).netloc

    def domain_allowed(self, url):
        domain = self.get_domain(url)
        for allowed in self.allowed_domains:
            if domain == allowed or domain.endswith("." + allowed):
                return True
        return False

    def worker(self):
        """Worker thread that continuously processes URLs."""
        while True:
            try:
                url, depth = self.queue.get(timeout=1)
            except Empty:
                return

            if len(self.visited) >= self.max_pages:
                return

            if url in self.visited:
                continue
            if depth > self.max_depth:
                continue
            if not self.domain_allowed(url):
                continue
            if not self.ignore_robots and not self.robots.allowed(url):
                continue


            self.visited.add(url)

            # Fetch page
            try:
                html = fetch(url)
            except Exception:
                continue

            
            if html is None:
                return
            
            title, meta, links = parse_html(html, url)
            print(f"[Crawled] {url} -> {title}")

            # Save page
            self.db.save(url, title, meta)

            # Enqueue next links
            if depth < self.max_depth:
                for link in links:
                    if link not in self.visited and self.domain_allowed(link):
                        self.queue.put((link, depth + 1))

    def start(self):
        # Seed the queue
        for s in self.seeds:
            self.queue.put((s, 0))

        # Spin up workers
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(self.worker) for _ in range(self.max_workers)]
            for f in futures:
                f.result()  # wait for all workers

