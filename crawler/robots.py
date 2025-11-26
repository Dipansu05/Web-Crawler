# crawler/robots.py
import urllib.robotparser
from urllib.parse import urljoin, urlparse

class RobotsChecker:
    def __init__(self, user_agent="WebCrawler"):
        self.user_agent = user_agent
        self.cache = {}

    def allowed(self, url):
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"

        if base not in self.cache:
            rp = urllib.robotparser.RobotFileParser()
            robots_url = urljoin(base, "/robots.txt")

            try:
                rp.set_url(robots_url)
                rp.read()
            except Exception:
                return True  # Fail-open (or change to False if strict)

            self.cache[base] = rp

        return self.cache[base].can_fetch(self.user_agent, url)
