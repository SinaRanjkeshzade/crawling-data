import sys
import logging
from selenium_crawler import SeleniumYouTubeCrawler
from parallel import parallel_crawl
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO)

def crawl_query(query, max_pages=3):
    with SeleniumYouTubeCrawler() as crawler:
        return crawler.crawl_search(query, max_pages=max_pages)

def print_results(all_results, queries):
    total = sum(len(r) for r in all_results)
    print(f"Crawled {total} videos across {len(queries)} queries:")
    for i, results in enumerate(all_results):
        print(f"\nResults for '{queries[i]}':")
        for video in results:
            print(f"Title: {video['title']}\nURL: {video['url']}\nTranscript: {video['transcript'][:200] if video['transcript'] else 'No transcript'}\n---")

def main():
    queries = ["python tutorials", "machine learning", "data science"]
    max_pages = 3
    try:
        # Parallel crawling for multiple queries
        args_list = [(q, max_pages) for q in queries]
        # Set max_workers=1 for single process
        all_results = parallel_crawl(crawl_query, args_list, max_workers=1)
        print_results(all_results, queries)
    except Exception as e:
        logging.error(f"Error in main: {e}")

def schedule_crawling():
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', hours=24)  # Run main() every 24 hours
    print("Scheduled crawling every 24 hours. Press Ctrl+C to exit.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'schedule':
        schedule_crawling()
    else:
        main()
