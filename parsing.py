import requests
from bs4 import BeautifulSoup
import csv
import time

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
TOTAL_PAGES = 7  # site has 50 pages

def get_soup(url):
    """Send GET request and return BeautifulSoup object"""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return None

def parse_book(book):
    """Extract data from a single book element"""
    title = book.h3.a["title"]
    price = book.find("p", class_="price_color").text
    availability = book.find("p", class_="instock availability").text.strip()
    rating_class = book.find("p")["class"]
    rating = rating_class[1] if len(rating_class) > 1 else "None"
    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating
    }

def parse_page(soup):
    """Parse all books on the page"""
    books = soup.find_all("article", class_="product_pod")
    return [parse_book(book) for book in books]

def save_to_csv(data, filename="books.csv"):
    """Save list of dicts to CSV"""
    if not data:
        print("❌ No data to save")
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Saved {len(data)} books to {filename}")

def scrape_books():
    """Main scraping function"""
    all_books = []
    for page in range(1, TOTAL_PAGES + 1):
        url = BASE_URL.format(page)
        print(f"🌐 Scraping page {page}: {url}")
        soup = get_soup(url)
        if soup:
            books = parse_page(soup)
            all_books.extend(books)
        time.sleep(1)  # polite crawling
    save_to_csv(all_books)

if __name__ == "__main__":
    scrape_books()
