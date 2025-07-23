from playwright.sync_api import sync_playwright
import json
import re

# Function to extract Schema.org data from the page
def extract_schema_data(page):
    """Extracts structured Schema.org data from the script tag."""
    try:
        schema_script = page.locator("script[type='application/ld+json']").inner_html()
        return json.loads(schema_script)
    except Exception as e:
        print(f"Error extracting schema data: {e}")
        return {}

# Extract title from Schema.org data
def extract_title(schema_data):
    """Extracts the book title."""
    return schema_data.get('name', 'Title not found')

# Extract authors from Schema.org data
def extract_authors(schema_data):
    """Extracts the list of authors."""
    try:
        return [author['name'] for author in schema_data.get('author', [])]
    except:
        return []

# Extract rating details from Schema.org data
def extract_rating(schema_data):
    """Extracts rating value and count."""
    aggregate_rating = schema_data.get('aggregateRating', {})
    return {
        'rating_value': aggregate_rating.get('ratingValue', 'N/A'),
        'rating_count': aggregate_rating.get('ratingCount', 'N/A')
    }

# Extract description from Schema.org data
def extract_description(schema_data):
    """Extracts the book description."""
    return schema_data.get('description', 'Description not found')

# Extract number of pages from Schema.org data
def extract_num_pages(schema_data):
    """Extracts the number of pages."""
    return schema_data.get('numberOfPages', 'N/A')

# Extract ISBN from Schema.org data
def extract_isbn(schema_data):
    """Extracts the ISBN from workExample."""
    work_example = schema_data.get('workExample', {})
    return work_example.get('isbn', 'ISBN not found')

# Extract genres from the page content
def extract_genres(page):
    """Extracts genres from the Genres section."""
    try:
        genres_header = page.locator("h3:has-text('Genres')")
        genres_container = genres_header.locator("xpath=..").locator("following-sibling::*[1]")
        genres = [genre.inner_text().strip() for genre in genres_container.locator("a").all()]
        return genres if genres else ['No genres found']
    except Exception:
        return ['Genres not found']

# Extract publication date from the page
def extract_publication_date(page):
    """Extracts the publication date from publication info."""
    try:
        publication_info = page.locator("p[data-testid='publicationInfo']").inner_text()
        match = re.search(r'\b(\w+ \d+, \d{4})\b', publication_info)
        return match.group(1) if match else 'Date not found'
    except Exception:
        return 'Publication date not found'

# Extract reading statistics from the page
def extract_reading_stats(page):
    """Extracts counts of people currently reading and wanting to read."""
    try:
        currently_reading_text = page.locator("text=/\d+ people are currently reading/").inner_text()
        want_to_read_text = page.locator("text=/\d+ people want to read/").inner_text()
        
        currently_reading = re.search(r'\d+', currently_reading_text).group()
        want_to_read = re.search(r'\d+', want_to_read_text).group()
        
        return {
            'currently_reading': int(currently_reading),
            'want_to_read': int(want_to_read)
        }
    except Exception:
        return {
            'currently_reading': 'N/A',
            'want_to_read': 'N/A'
        }

# Extract suggested books from the page
def extract_suggested_books(page):
    """Extracts titles of suggested books under 'Readers also enjoyed'."""
    try:
        suggested_header = page.locator("h3:has-text('Readers also enjoyed')")
        suggested_container = suggested_header.locator("xpath=..").locator("following-sibling::*[1]")
        suggested_books = [book.inner_text().strip() for book in suggested_container.locator("a").all()]
        return suggested_books if suggested_books else ['No suggested books found']
    except Exception:
        return ['Suggested books not found']

# Extract edition details from the page
def extract_edition_details(page):
    """Extracts details about the current edition."""
    try:
        edition_header = page.locator("h4:has-text('This edition')")
        edition_container = edition_header.locator("xpath=..").locator("following-sibling::*[1]")
        details = edition_container.inner_text().strip()
        return details if details else 'Edition details not found'
    except Exception:
        return 'Edition details not found'

# Extract links to other editions
def extract_other_editions_links(page):
    """Extracts URLs to other editions."""
    try:
        editions_header = page.locator("h4:has-text('More editions')")
        editions_container = editions_header.locator("xpath=..").locator("following-sibling::*[1]")
        links = [link.get_attribute("href") for link in editions_container.locator("a").all()]
        return links if links else ['No other editions found']
    except Exception:
        return ['Other editions not found']

# Extract more information tags
def extract_more_information(page):
    """Extracts additional information under 'More information'."""
    try:
        info_header = page.locator("h4:has-text('More information')")
        info_container = info_header.locator("xpath=..").locator("following-sibling::*[1]")
        info_text = info_container.inner_text().strip()
        return info_text if info_text else 'No additional info found'
    except Exception:
        return 'More information not found'

# Main scraping function
def scrape_goodreads_page(url):
    """Scrapes all information from the specified Goodreads page."""
    with sync_playwright() as p:
        # Launch browser and navigate to the page
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        
        # Wait for main content to load
        page.wait_for_selector("div.BookPage__mainContent", timeout=40000)
        
        # Extract Schema.org data
        schema_data = extract_schema_data(page)
        
        # Compile all book information
        book_info = {
            'title': extract_title(schema_data),
            'authors': extract_authors(schema_data),
            'rating': extract_rating(schema_data),
            'description': extract_description(schema_data),
            'num_pages': extract_num_pages(schema_data),
            'isbn': extract_isbn(schema_data),
            'genres': extract_genres(page),
            'publication_date': extract_publication_date(page),
            'reading_stats': extract_reading_stats(page),
            'edition_details': extract_edition_details(page),
            'other_editions_links': extract_other_editions_links(page),
            'more_information': extract_more_information(page),
            'suggested_books': extract_suggested_books(page)
        }
        
        # Close the browser
        browser.close()
        
        return book_info


url = "https://www.goodreads.com/book/show/61273823-take-command?ref=rae_1"
try:
    data = scrape_goodreads_page(url)
    print(json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"An error occurred: {e}")