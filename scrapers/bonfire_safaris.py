import sys
import os
import re
from playwright.sync_api import sync_playwright, TimeoutError

# Allow project imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.insert_travel_package import insert_travel_package

BASE_URL = "https://bonfireadventures.com"

CATEGORY_URLS = [

    # Safaris
    {"url": "/package_category/private_wildlife_safaris", "type": "Safari"},

    # Destinations - Africa
    {"url": "/destination_country/Kenya", "type": "Destination"},
    {"url": "/destination_country/Mauritius", "type": "Destination"},
    {"url": "/destination_country/Tanzania", "type": "Destination"},
    {"url": "/destination_country/South%20Africa", "type": "Destination"},

    # Destinations - Middle East / Asia
    {"url": "/destination_country/United%20Arab%20Emirates", "type": "Destination"},
    {"url": "/destination_country/Pakistan", "type": "Destination"},
    {"url": "/destination_country/China", "type": "Destination"},
    {"url": "/destination_country/Singapore", "type": "Destination"},

    # Local Packages
    {"url": "/packages", "type": "Local"},
]


# ----------------------------
# Helpers
# ----------------------------

def clean_price(text):
    if not text:
        return None
    numbers = re.sub(r"[^\d.]", "", text)
    return float(numbers) if numbers else None


def extract_duration(title):
    match = re.search(r"(\d+)\s*DAY", title.upper())
    if match:
        return f"{match.group(1)} Days"
    return None


def extract_destination(title):

    keywords = [
        "Maasai Mara", "Amboseli", "Samburu", "Tsavo",
        "Nakuru", "Naivasha", "Mt Kenya",
        "Tanzania", "Zanzibar",
        "Dubai", "United Arab Emirates",
        "South Africa", "Mauritius",
        "Thailand", "Malaysia", "Singapore",
        "China", "Pakistan",
        "Diani", "Mombasa"
    ]

    for word in keywords:
        if word.lower() in title.lower():
            return word

    return "Kenya"


# ----------------------------
# Scraper
# ----------------------------

def scrape_category(page, category):
    full_url = BASE_URL + category["url"]
    category_type = category["type"]

    print(f"\nScraping: {full_url} | Type: {category_type}")

    try:
        page.goto(full_url, wait_until="load", timeout=60000)
        page.wait_for_load_state("networkidle")
    except TimeoutError:
        print("⚠️ Page load timeout — continuing anyway...")

    page.wait_for_timeout(5000)

    cards = page.locator("div:has(h3)")
    count = cards.count()

    print(f"Found {count} cards")

    seen_titles = set()

    for i in range(count):
        card = cards.nth(i)

        title_locator = card.locator("h3")
        if title_locator.count() == 0:
            continue

        title = title_locator.first.inner_text().strip()

        # Skip layout garbage
        if len(title) < 10 or "Available Packages" in title:
            continue

        # Prevent duplicates in same run
        if title in seen_titles:
            continue

        seen_titles.add(title)

        card_text = card.inner_text()

        # ------------------
        # Price extraction
        # ------------------
        price_match = re.search(r"USD\s?[\d,]+", card_text)
        if not price_match:
            price_match = re.search(r"USD[\d,]+", card_text)

        price = clean_price(price_match.group()) if price_match else None

        # ------------------
        # Rating extraction
        # ------------------
        rating = None
        rating_match = re.search(r"\b\d\.\d\b", card_text)
        if rating_match:
            rating = float(rating_match.group())

        duration = extract_duration(title)
        destination = extract_destination(title)

        data = {
            "package_name": title,
            "price_usd": price,
            "duration": duration,
            "company": "Bonfire Adventures",
            "destination": destination,
            "source": "Bonfire Adventures",
            "rating": rating,
            "category_type": category_type,
        }

        print(
            f"Inserting/Updating: {title} | "
            f"Price: {price} | "
            f"Rating: {rating} | "
            f"Type: {category_type}"
        )

        insert_travel_package(data)


# ----------------------------
# Main
# ----------------------------

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"
        )

        page = context.new_page()

        for category in CATEGORY_URLS:
            scrape_category(page, category)

        browser.close()

    print("\nFinished scraping all categories.")


if __name__ == "__main__":
    main()