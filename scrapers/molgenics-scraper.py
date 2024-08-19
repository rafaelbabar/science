#OneDrive\Desktop\Projects\science\pages\scrapers>python molgenics-scraper.py


from playwright.sync_api import sync_playwright
import json

def fetch_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run in non-headless mode
        page = browser.new_page()

        try:
            # Initialize an empty list to hold all structured data
            all_structured_data = []

            page_number = 1
            while True:
                page_url = f"https://molgenics.co.uk/index.php?route=product/catalog&limit=100&page={page_number}"
                page.goto(page_url, timeout=60000)
                page.wait_for_timeout(10000)  # Wait 10 seconds for JavaScript to load completely

                # Example: Extract addresses, prices, and property links
                products = page.query_selector_all('div.name') if page.query_selector('div.name') else []
                descriptions = page.query_selector_all('div.description') if page.query_selector('div.description') else []
                prices = page.query_selector_all('span.price-normal') if page.query_selector('span.price-normal') else []
                links = page.query_selector_all('div.name a')

                # If no products found, break the loop (end of pagination)
                if not products:
                    break

                base_url = "https://molgenics.co.uk/"

                for product, description, price, link in zip(products, descriptions, prices, links):
                    product_text = product.text_content().strip().replace("\u00a0", " ")
                    price_text = price.text_content().strip().replace("\u00a3", "£")
                    raw_link = link.get_attribute('href').strip()
                    if raw_link.startswith('http'):
                        final_link = raw_link
                    else:
                        final_link = base_url + raw_link

                    # Append structured data from the current page to the list
                    all_structured_data.append({
                        'product': product_text,
                        'description': description.text_content().strip() if description else '',
                        'price': price_text,
                        'link': final_link
                    })

                # Increment the page number for the next iteration
                page_number += 1

            # Writing to JSON
            with open('molgenics.json', 'w', encoding='utf-8') as f:
                json.dump(all_structured_data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"An error occurred: {e}")

fetch_data()


