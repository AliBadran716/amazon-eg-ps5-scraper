# 🛒 Amazon Egypt PS5 Games Web Scraper

This is a Python-based web scraper that collects product data for **PS5 games from Amazon Egypt** (`amazon.eg`) using Selenium and BeautifulSoup. It extracts:

- 🏷️ Product Names  
- 💰 Prices  
- ⭐ Ratings  
- 📝 Number of Reviews  
- 🔗 Product Links  
- 🖼️ Image URLs

The results are saved in a CSV file called `amazon_ps5_games.csv`.

---

## 📦 Features

- Scrapes multiple pages (currently set to 5 pages).
- Stores data neatly in a CSV format.
- Uses **headless browsing** (runs in the background).
- Includes smart waiting to ensure content loads before scraping.

---

## 🚀 How to Run

1. **Install dependencies** (you can use a virtual environment if you want):

```bash
pip install selenium webdriver-manager beautifulsoup4
````

2. **Run the script**:

```bash
python amazon_scraper.py
```

After it completes, you’ll find the scraped data in `amazon_ps5_games.csv`.

---

## ⚠️ Known Issues

* ❌ **Unstable behavior**: Sometimes the script fails due to Amazon’s anti-bot measures, network delays, or dynamic content changes.
* ✅ **Quick Fix**: Just run the script again. It usually works after a retry or two.

---

## 📁 Output Format

The script saves data in this format:

| Product Name | Price | Rating | Reviews | Product Link | Image Link |
| ------------ | ----- | ------ | ------- | ------------ | ---------- |

---

## 🧠 Tech Stack

* `Selenium` for dynamic content loading
* `BeautifulSoup` for HTML parsing
* `WebDriverManager` for auto-managing ChromeDriver

---

## 📝 License

This scraper is for educational purposes only. Do not use it to violate Amazon’s [Terms of Service](https://www.amazon.com/gp/help/customer/display.html?nodeId=201909000).

---

## 🤖 Author

Ali Badran

