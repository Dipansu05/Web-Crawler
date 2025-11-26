import argparse
from crawler.crawler import Crawler


def cli():
    parser = argparse.ArgumentParser(description="Simple multi-threaded crawler")
    parser.add_argument("seeds", nargs="+", help="Seed URLs to start from")
    parser.add_argument("--workers", type=int, default=5)
    parser.add_argument("--max-pages", type=int, default=50)
    parser.add_argument("--depth", type=int, default=2)
    return parser.parse_args()


if __name__ == "__main__":
    args = cli()
    crawler = Crawler(
        seeds=args.seeds,
        max_workers=args.workers,
        max_pages=args.max_pages,
        max_depth=args.depth,
    )
    crawler.start()

