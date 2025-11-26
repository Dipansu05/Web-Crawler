import argparse
from crawler.crawler import Crawler

def cli():
    p = argparse.ArgumentParser(description="Multi-threaded crawler")
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
    )
    crawler.start()
