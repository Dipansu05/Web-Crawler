# utils/db.py
import sqlite3
import json
from datetime import datetime

class CrawlerDB:
    def __init__(self, path="crawler.db"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init()

    def _init(self):
        c = self.conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            title TEXT,
            meta TEXT,
            crawled_at TEXT
        )
        """)
        self.conn.commit()

    def save(self, url, title, meta):
        c = self.conn.cursor()
        c.execute("""
        INSERT OR REPLACE INTO pages (url, title, meta, crawled_at)
        VALUES (?, ?, ?, ?)
        """, (url, title, json.dumps(meta), datetime.utcnow().isoformat()))
        self.conn.commit()

    def export_json(self, outfile="output.json"):
        c = self.conn.cursor()
        c.execute("SELECT url, title, meta, crawled_at FROM pages")

        data = []
        for row in c.fetchall():
            url, title, meta, ts = row
            data.append({
                "url": url,
                "title": title,
                "meta": json.loads(meta),
                "crawled_at": ts
            })

        with open(outfile, "w") as f:
            json.dump(data, f, indent=2)

    def close(self):
        self.conn.close()

