#OneDrive\Desktop\Projects\science\pages\scrapers>python molgenics-scraper.py

from playwright.sync_api import sync_playwright
import json

def fetch_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run in non-headless mode
        page = browser.new_page()

        try:
            page.goto("https://molgenics.co.uk/index.php?route=product/catalog&limit=100", timeout=60000)  # 60 seconds timeout
            page.wait_for_timeout(10000)  # Wait 10 seconds for JavaScript to load completely

            # Extract product information
            products = page.query_selector_all('div.name') if page.query_selector('div.name') else []
            descriptions = page.query_selector_all('div.description') if page.query_selector('div.description') else []
            prices = page.query_selector_all('span.price-normal') if page.query_selector('span.price-normal') else []
            links = page.query_selector_all('div.name a')

            # Debug output
            print(f"Found {len(products)} products")
            print(f"Found {len(descriptions)} descriptions")
            print(f"Found {len(prices)} prices")
            print(f"Found {len(links)} links")

            # List to hold structured data
            structured_data = []

            base_url = "https://molgenics.co.uk/"

            for product, description, price, link in zip(products, descriptions, prices, links):
                # Clean up the products and price strings
                product_text = product.text_content().strip().replace("\u00a0", " ")
                price_text = price.text_content().strip().replace("\u00a3", "£")

                # Extract and clean the link
                raw_link = link.get_attribute('href').strip()
                
                # Ensure no duplication of base URL
                if raw_link.startswith('http'):
                    final_link = raw_link
                else:
                    final_link = base_url + raw_link

                # Debug output for each entry
                print(f"Product: {product_text}, Price: {price_text}, Link: {final_link}")

                # Append structured data
                structured_data.append({
                    'product': product_text,
                    'description': description.text_content().strip() if description else '',
                    'price': price_text,
                    'link': final_link
                })

            # Writing to JSON
            with open('molgenics.json', 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"An error occurred: {e}")

fetch_data()
