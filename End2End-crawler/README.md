# Advanced YouTube Crawler

This project provides an advanced YouTube crawler that can:
- Crawl public YouTube search results using Selenium (browser automation)
- Fetch video data using the official YouTube Data API (requires API key)
- Handle pagination, session management, and basic CAPTCHA detection
- Run multiple crawls in parallel for efficiency
- Use a proxy for transcript fetching (WebshareProxyConfig)

## Features
- **Selenium Crawler:** Crawls YouTube search results, handles dynamic content, pagination, and session cookies.
- **API Client:** Fetches video data using the YouTube Data API (structured, reliable, but requires API key).
- **Parallel Processing:** Crawl multiple queries at once for speed.
- **CAPTCHA Detection:** Stops and logs if a CAPTCHA is detected (no bypass).
- **Proxy Support:** Fetches YouTube transcripts via a proxy (WebshareProxyConfig).

## Installation
1. Clone this repository or copy the code to your machine.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (For Selenium) Make sure you have Google Chrome installed. The `webdriver-manager` package will auto-download the correct ChromeDriver.

## Proxy Configuration (IMPORTANT)
To fetch YouTube transcripts, the crawler uses a proxy via [WebshareProxyConfig](https://github.com/jdepoix/youtube-transcript-api#proxies). **You must set your proxy credentials** in `selenium_crawler.py`:

```
proxy_config=WebshareProxyConfig(
    proxy_username="YOUR_PROXY_USERNAME",
    proxy_password="YOUR_PROXY_PASSWORD",
)
```
- Get your proxy credentials from your proxy provider (e.g., [webshare.io](https://www.webshare.io/)).
- If you do not set these, transcript fetching will not work.

## Usage

### 1. Crawling with Selenium (No API Key Needed)
By default, `crawler.py` uses Selenium to crawl public YouTube search results for multiple queries in parallel.

Run:
```bash
python crawler.py
```

- Results will be printed to the console.
- To crawl different queries, edit the `queries` list in `crawler.py`.
- To change the number of pages per query, edit the `max_pages` variable in `crawler.py`.
- If you need to crawl authenticated content, export your cookies and pass them to `SeleniumYouTubeCrawler` (see the class docstring in `selenium_crawler.py`).
- **Proxy credentials must be set as described above.**

#### Scheduled Crawling
To run the crawler automatically every 24 hours:
```bash
python crawler.py schedule
```

### 2. Crawling with YouTube Data API (Requires API Key)
To use the API client:
- Get a YouTube Data API v3 key from the [Google Cloud Console](https://console.developers.google.com/).
- Use the `YouTubeAPIClient` class in `api_client.py`:

```python
from api_client import YouTubeAPIClient
api_key = 'YOUR_API_KEY'
client = YouTubeAPIClient(api_key)
results = client.search_videos('python tutorials', max_results=10)
for video in results:
    print(video)
```

### 3. Running the Selenium Crawler Directly
You can also run the Selenium crawler directly for a single query:
```bash
python selenium_crawler.py
```
- This will crawl the default query ("python tutorials").
- To customize, modify the code at the bottom of `selenium_crawler.py`.

### 4. Parallel Crawling
The crawler supports parallel crawling of multiple queries using Python's `concurrent.futures` (see `parallel.py`).
- By default, `crawler.py` uses a single worker (`max_workers=1`).
- To increase parallelism, change `max_workers` in `crawler.py`.

### 5. Temporary Scripts
- `temp.py` contains example code for browser automation and is not required for main crawling tasks.

## Notes
- **Proxy Required:** You must set your proxy username and password in `selenium_crawler.py` for transcript fetching to work.
- **Parallel Crawling:** The crawler can crawl multiple queries at once.
- **CAPTCHA Handling:** If a CAPTCHA is detected, crawling will stop and log an error. Bypassing CAPTCHA is not supported.
- **ChromeDriver:** Managed automatically by `webdriver-manager`.
- **API Quotas:** The YouTube Data API is free for limited use. Heavy usage may require payment.

## Troubleshooting
- If you see `Import "selenium" could not be resolved`, ensure you installed all requirements and are using the correct Python environment.
- If ChromeDriver issues occur, ensure your Chrome browser is up to date.
- If transcript fetching fails, check your proxy credentials in `selenium_crawler.py`.
- For proxy issues, verify your proxy provider and network settings.

## License
MIT 