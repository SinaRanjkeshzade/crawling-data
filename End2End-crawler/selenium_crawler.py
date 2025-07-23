import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

logging.basicConfig(level=logging.INFO)

# Try to use undetected-chromedriver for stealth, fallback to normal Chrome
try:
    import undetected_chromedriver as uc
    USE_UC = True
except ImportError:
    USE_UC = False

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]

def human_like_scroll(driver, total_scrolls=5):
    """Scrolls the page in a human-like way."""
    for _ in range(total_scrolls):
        scroll_amount = random.randint(200, 800)
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        time.sleep(random.uniform(1.0, 3.0))

def human_like_mouse_move(driver):
    """Moves the mouse to a random element to simulate human behavior."""
    actions = ActionChains(driver)
    elements = driver.find_elements(By.CSS_SELECTOR, "a, button, input")
    if elements:
        element = random.choice(elements)
        actions.move_to_element(element).perform()
        time.sleep(random.uniform(0.5, 1.5))

class SeleniumYouTubeCrawler:
    """
    Crawler for YouTube using Selenium. Handles pagination, cookies, authentication, CAPTCHA detection, and human-mimicry.
    """
    def __init__(self, headless=True, cookies=None):
        user_agent = random.choice(USER_AGENTS)
        chrome_binary = "/opt/google/chrome/chrome"
        
        # Set up Chrome options
        options = uc.ChromeOptions()
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless' if headless else '')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')  # Added for stability in headless mode
        
        # Enable ChromeDriver logging for debugging
        service = Service(log_path="chromedriver.log")
        
        # Initialize the driver
        self.driver = uc.Chrome(
            service=service,
            options=options,
            browser_executable_path=chrome_binary
        )
        self.cookies = cookies or []
        self._load_cookies()

    def _load_cookies(self):
        """Load cookies into the browser for session management."""
        if self.cookies:
            self.driver.get("https://www.youtube.com")
            for cookie in self.cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    logging.warning(f"Failed to add cookie: {e}")

    def login(self, email, password):
        """Optional: Log in to YouTube for authenticated crawling."""
        logging.info("Login not implemented for security. Use cookies if needed.")

    def get_transcript(self, video_url, languages=['en']):
        """Fetch transcript for a given YouTube video URL. Returns transcript as text or None if not available."""
        import re
        match = re.search(r"v=([\w-]+)", video_url)
        if not match:
            return None
        video_id = match.group(1)
        try:
            transcript = YouTubeTranscriptApi.fetch(video_id, languages=languages)
            return " ".join([seg['text'] for seg in transcript])
        except (TranscriptsDisabled, NoTranscriptFound):
            return None
        except Exception as e:
            logging.warning(f"Transcript fetch error for {video_url}: {e}")
            return None

    def crawl_search(self, query, max_pages=1):
        """Crawl YouTube search results for a given query, including transcripts."""
        results = []
        url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        try:
            self.driver.get(url)
            time.sleep(random.uniform(2.0, 4.0))  # Initial random delay
            for page in range(max_pages):
                human_like_scroll(self.driver, total_scrolls=random.randint(2, 5))
                human_like_mouse_move(self.driver)
                time.sleep(random.uniform(2.0, 5.0))
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_any_elements_located((By.ID, 'video-title'))
                    )
                except Exception as e:
                    logging.error(f"Timeout waiting for video elements: {e}")
                    continue
                videos = self.driver.find_elements(By.ID, 'video-title')
                for video in videos:
                    try:
                        if video.is_displayed() and video.is_enabled():
                            title = video.get_attribute('title')
                            href = video.get_attribute('href')
                            if title and href:
                                transcript = self.get_transcript(href)
                                results.append({'title': title, 'url': href, 'transcript': transcript})
                    except Exception as e:
                        logging.error(f"Error accessing video element: {e}")
        except WebDriverException as e:
            logging.error(f"WebDriver error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        return results

    def detect_captcha(self):
        """Detect if a CAPTCHA is present."""
        try:
            if "captcha" in self.driver.page_source.lower():
                return True
            self.driver.find_element(By.XPATH, "//iframe[contains(@src, 'recaptcha')]")
            return True
        except NoSuchElementException:
            return False
        except Exception as e:
            logging.warning(f"Error during CAPTCHA detection: {e}")
            return False

    def close(self):
        """Close the driver."""
        try:
            self.driver.quit()
        except Exception as e:
            logging.warning(f"Error closing driver: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# Example usage
if __name__ == "__main__":
    crawler = SeleniumYouTubeCrawler(headless=True)
    results = crawler.crawl_search("python tutorials", max_pages=1)
    for result in results:
        print(f"Title: {result['title']}, URL: {result['url']}")
    crawler.close()