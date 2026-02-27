from playwright.sync_api import sync_playwright
from db.insert_destinations import insert_destination

BASE_URL = "https://magicalkenya.com"
PLACES_URL = "https://magicalkenya.com/places-to-go/"

# ---------------------------------------------------
# REGION NORMALIZATION
# ---------------------------------------------------
REGION_MAP = {
    "Central Highlands": "Central Highlands",
    "Eastern Kenya": "Eastern",
    "Great Rift Valley": "Rift Valley",
    "Mombasa and South Coast": "Coast South",
    "Nairobi Circuit": "Nairobi",
    "North Coast": "Coast North",
    "Northern Kenya": "Northern",
    "South Eastern": "South Eastern",
    "Southern Kenya": "Southern",
    "Western Kenya": "Western"
}


# ---------------------------------------------------
# CLEAN CATEGORY FROM CLASS STRING
# ---------------------------------------------------
def clean_category_from_class(class_string):
    """
    Extract category from class attribute.
    Example:
    category-game-parks-reserves -> Game Parks & Reserves
    """

    if not class_string:
        return "Other"

    classes = class_string.split()

    for cls in classes:
        if cls.startswith("category-"):
            raw = cls.replace("category-", "")
            formatted = raw.replace("-", " ").title()

            # Improve formatting
            formatted = formatted.replace("And", "&")

            return formatted

    return "Other"


# ---------------------------------------------------
# MAIN SCRAPER
# ---------------------------------------------------
def scrape_experiences():
    results = []
    all_experience_links = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(PLACES_URL, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(5000)

        # Get region options from hidden select
        options = page.query_selector_all("select[name='region'] option")

        print(f"\nFound {len(options)} region options.\n")

        # Loop through each region
        for option in options:
            value = option.get_attribute("value")
            region_label = option.inner_text().strip()

            if not value:
                continue  # Skip default option

            normalized_region = REGION_MAP.get(region_label, region_label)

            print(f"Selecting region: {region_label}")

            # Force select region (hidden select)
            page.select_option(
                "select[name='region']",
                value=value,
                force=True
            )

            page.wait_for_timeout(6000)

            # Collect experience links for this region
            links = page.query_selector_all("a")

            for link in links:
                href = link.get_attribute("href")

                if href and href.startswith(BASE_URL) and "/experience/" in href:
                    all_experience_links[href] = normalized_region

        print(f"\nTotal unique experiences found: {len(all_experience_links)}\n")

        # ---------------------------------------------------
        # Visit each experience page
        # ---------------------------------------------------
        for url, region_name in all_experience_links.items():
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2500)

            title_element = page.query_selector(".elementor-heading-title")
            paragraphs = page.query_selector_all(
                ".elementor-widget-theme-post-content p"
            )

            # 🔥 CORRECT CATEGORY EXTRACTION
            container = page.query_selector(
                "div[data-elementor-type='single-post']"
            )
            container_class = container.get_attribute("class") if container else ""
            category = clean_category_from_class(container_class)

            if not title_element:
                continue

            title = " ".join(title_element.inner_text().split()).title()

            description = ""
            for p_tag in paragraphs[:3]:
                text = p_tag.inner_text().strip()
                if text:
                    description += text + " "

            description = description.strip()

            print(f"Inserting: {title} | {region_name} | {category}")

            insert_destination({
                "name": title,
                "county": region_name,
                "category": category,
                "description": description,
                "source": "Magical Kenya"
            })

            results.append({
                "name": title,
                "region": region_name,
                "category": category
            })

            page.wait_for_timeout(1000)

        browser.close()

    return results


# ---------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------
def main():
    data = scrape_experiences()

    print("\nFinished inserting experiences.")
    print(f"Total processed: {len(data)}\n")


if __name__ == "__main__":
    main()