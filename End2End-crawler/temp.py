import logging
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from contextlib import contextmanager
import os
import pathlib

logging.basicConfig(level=logging.INFO)

# Try to use undetected-chromedriver for stealth, fallback to normal Chrome
try:
    import undetected_chromedriver as uc
    USE_UC = True
except ImportError:
    USE_UC = False

USER_AGENTS = [
    # A few common user agents
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

user_agent = random.choice(USER_AGENTS)
chrome_binary = "/opt/google/chrome/chrome"
options = uc.ChromeOptions()
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--headless')         # Run Chrome without GUI
options.add_argument('--disable-gpu')      # Disable GPU acceleration (often needed with headless)
# For undetected-chromedriver, use browser_executable_path
driver = uc.Chrome(options=options , browser_executable_path=chrome_binary)
driver.get("https://www.goodreads.com/book/show/17912916-data-science-for-business?from_search=true&from_srp=true&qid=EVSW0x6JUR&rank=1")
print("Done")
