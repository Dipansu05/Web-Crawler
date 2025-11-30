import argparse
from crawler.crawler import Crawler

def cli():
    p = argparse.ArgumentParser(description="Multi-threaded crawler")
    p.add_argument("--export-json", action="store_true", help="Export SQLite data to JSON after crawl")
    p.add_argument("--ignore-robots", action="store_true", help="Disable robots.txt checking")
    p.add_argument("seeds", nargs="+")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--max-pages", type=int, default=200)
    p.add_argument("--depth", type=int, default=2)
    return p.parse_args()

if __name__ == "__main__":
    args = cli()

    crawler = Crawler(
        seeds=args.seeds,
        max_workers=args.workers,
        max_pages=args.max_pages,
        max_depth=args.depth,
        ignore_robots=args.ignore_robots
    )

    crawler.start()

    # Export JSON AFTER crawling
    if args.export_json:
        from utils.db import CrawlerDB
        db = CrawlerDB("crawler.db")
        db.export_json("output.json")
        print("Exported JSON -> output.json")
