from urllib.parse import urljoin
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_article_urls_from_homepage(base_url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(base_url)
        html = await page.content()
        await browser.close()

        soup = BeautifulSoup(html, "html.parser")
        raw_links = [a['href'] for a in soup.select("a") if a.get('href')]

        # Only keep links that match article-like patterns
        filtered_links = []
        for href in raw_links:
            full_url = urljoin(base_url, href)
            if "/20" in full_url and full_url.startswith("https://www.nytimes.com"):
                filtered_links.append(full_url)

        return list(set(filtered_links))  # Remove duplicates
