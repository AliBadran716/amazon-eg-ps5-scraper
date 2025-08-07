from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv
from itertools import zip_longest

# Setup Chrome options for headless browsing which allows running Chrome in the background without UI.
options = Options()
options.add_argument("--headless")  # Run Chrome in headless mode.
options.add_argument("--no-sandbox")  # Bypass OS security model, needed for some environments.
options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in containers.

# Initialize the Chrome webdriver using the ChromeDriverManager to automatically manage driver binaries.
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Base URL template for Amazon Egypt PS5 games search results pages.
base_url = "https://www.amazon.eg/s?k=ps5+games&page={}"

# Lists to store scraped data from all the pages.
all_names = []    # Stores product titles.
all_prices = []   # Stores product prices.
all_ratings = []  # Stores product ratings (e.g., "4.5 out of 5 stars").
all_reviews = []  # Stores the number of customer reviews.
all_links = []    # Stores URLs to the product detail pages.
all_images = []   # Stores URLs to product images.

# Scraping loop for the first 5 pages (can be adjusted).
for page in range(1, 6):
    print(f"🔄 Scraping page {page}...")

    # Load the page using Selenium.
    driver.get(base_url.format(page))
    # Wait until at least one product name appears (max 10 seconds)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "a-size-base-plus"))
    )

    # Parse the page content with BeautifulSoup for easy HTML traversal.
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract product names from h2 tags with the specified class.
    product_names = [tag.text.strip() for tag in soup.find_all("h2", class_="a-size-base-plus a-spacing-none a-color-base a-text-normal")]
    all_names.extend(product_names)

    # Extract prices by looking inside span tags with class "a-price", combining whole and fractional part.
    for price_tag in soup.find_all("span", class_="a-price"):
        whole = price_tag.find("span", class_="a-price-whole")
        frac = price_tag.find("span", class_="a-price-fraction")
        # Only append price if both whole and fractional parts exist.
        if whole and frac:
            all_prices.append(whole.text.strip() + "." + frac.text.strip())
        else:
            all_prices.append("")  # Append empty string if price is missing.

    # Extract ratings from span tags with class "a-icon-alt" (ratings are usually in this format).
    ratings = [tag.text.strip() for tag in soup.find_all("span", class_="a-icon-alt")]
    all_ratings.extend(ratings)

    # Extract number of reviews from spans with class "a-size-base s-underline-text".
    reviews = [tag.text.strip() for tag in soup.find_all("span", class_="a-size-base s-underline-text")]
    all_reviews.extend(reviews)

    # Extract product detail page links from anchor tags with class "a-link-normal s-no-outline".
    for tag in soup.find_all("a", class_="a-link-normal s-no-outline"):
        link = tag.get("href")
        if link:
            # Construct full URL by prepending base domain.
            all_links.append("https://www.amazon.eg" + link)

    # Extract product image URLs from img tags with class "s-image".
    image_links = [tag.get("src") for tag in soup.find_all("img", class_="s-image")]
    all_images.extend(image_links)

# Close the Selenium WebDriver session.
driver.quit()

# Ensure all lists have the same length by filling missing entries with empty strings.
max_len = max(len(all_names), len(all_prices), len(all_ratings), len(all_reviews), len(all_links), len(all_images))
all_data = zip_longest(all_names, all_prices, all_ratings, all_reviews, all_links, all_images, fillvalue="")

# Save the collected data into a CSV file using UTF-8 encoding.
with open("amazon_ps5_games.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write the header row for clarity.
    writer.writerow(["Product Name", "Price", "Rating", "Reviews", "Product Link", "Image Link"])
    # Write the scraped product data rows.
    writer.writerows(all_data)

print("✅ Scraping completed. Saved ~100 products to amazon_ps5_games.csv")