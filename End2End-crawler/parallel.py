from concurrent.futures import ProcessPoolExecutor, as_completed
import logging

def parallel_crawl(crawl_func, args_list, max_workers=4):
    """
    Run crawl_func in parallel with different arguments. Logs errors and returns empty results for failed processes.
    """
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        future_to_args = {executor.submit(crawl_func, *args): args for args in args_list}
        for future in as_completed(future_to_args):
            args = future_to_args[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logging.error(f"Error in process for args {args}: {e}")
                results.append([])
    return results 