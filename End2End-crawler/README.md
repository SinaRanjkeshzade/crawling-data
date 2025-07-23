# Advanced YouTube Crawler

This project provides an advanced YouTube crawler that can:
- Crawl public YouTube search results using Selenium (browser automation)
- Fetch video data using the official YouTube Data API (requires API key)
- Handle pagination, session management, and basic CAPTCHA detection
- Run multiple crawls in parallel for efficiency

## Features
- **Selenium Crawler:** Crawls YouTube search results, handles dynamic content, pagination, and session cookies.
- **API Client:** Fetches video data using the YouTube Data API (structured, reliable, but requires API key).
- **Parallel Processing:** Crawl multiple queries at once for speed.
- **CAPTCHA Detection:** Stops and logs if a CAPTCHA is detected (no bypass).

## Installation
1. Clone this repository or copy the code to your machine.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (For Selenium) Make sure you have Google Chrome installed. The `webdriver-manager` package will auto-download the correct ChromeDriver.

## Usage

### 1. Crawling with Selenium (No API Key Needed)
By default, `crawler.py` uses Selenium to crawl public YouTube search results for multiple queries in parallel.

Run:
```bash
python crawler.py
```

- Results will be printed to the console.
- To crawl different queries, edit the `queries` list in `crawler.py`.
- If you need to crawl authenticated content, export your cookies and pass them to `SeleniumYouTubeCrawler`.

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

### Notes
- **Parallel Crawling:** The crawler uses threads to crawl multiple queries at once.
- **CAPTCHA Handling:** If a CAPTCHA is detected, crawling will stop and log an error. Bypassing CAPTCHA is not supported.
- **ChromeDriver:** Managed automatically by `webdriver-manager`.
- **API Quotas:** The YouTube Data API is free for limited use. Heavy usage may require payment.

## Troubleshooting
- If you see `Import "selenium" could not be resolved`, ensure you installed all requirements and are using the correct Python environment.
- If ChromeDriver issues occur, ensure your Chrome browser is up to date.

## License
MIT 