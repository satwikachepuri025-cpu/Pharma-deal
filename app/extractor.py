import cloudscraper
import trafilatura
from playwright.sync_api import sync_playwright


def fetch_with_playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=15000)
            html = page.content()
            browser.close()
            return html
    except Exception as e:
        print("❌ Playwright fetch error:", e)
        return None


def extract_article_text(url):
    try:
        print(f"\n🔗 Original URL: {url}")

        scraper = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "darwin",
                "mobile": False
            }
        )

        response = scraper.get(url, timeout=15)

        print(f"➡ Final URL after redirect: {response.url}")
        print(f"➡ Status Code: {response.status_code}")

        html_content = None

        if response.status_code == 200 and response.text:
            html_content = response.text
        else:
            print("⚠ cloudscraper blocked — using Playwright fallback.")
            html_content = fetch_with_playwright(url)

        if not html_content:
            print("❌ Failed to retrieve HTML content.")
            return None

        text = trafilatura.extract(html_content)

        if not text:
            print("❌ Extraction returned empty text.")
            return None

        print(f"➡ Extracted text length: {len(text)}")
        return text

    except Exception as e:
        print("❌ Exception:", e)
        return None