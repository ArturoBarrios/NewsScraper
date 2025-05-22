from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from urllib.parse import urlparse, urlunparse
import random
from datetime import datetime

from .ArticlesCommon import send_to_processing_backend


async def extract_article_data(url: str):
    print("🔎 Extracting article data from:", url)
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            html = await page.content()
            await browser.close()

        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
        date = datetime.utcnow().isoformat() + "Z"

        paragraphs = soup.select("section[name='articleBody'] p")
        if not paragraphs:
            paragraphs = soup.select("article p")

        content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        parsed_url = urlparse(url)
        unique_url = urlunparse(parsed_url._replace(query="", fragment=""))
        unique_url = f"{unique_url}?rand={random.randint(100000, 999999)}"

        article = {
            "url": unique_url,
            "title": title,
            "date": date,
            "content": content
        }

        print(f"✅ Extracted article: {title}")
        send_to_processing_backend(article)
        return article

    except Exception as e:
        print(f"❌ Failed to extract article from {url}: {e}")
        return None

async def scrape_nytimes_homepage():
    print("🌐 Scraping NYTimes homepage for story links...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto("https://www.nytimes.com", timeout=60000)
            html = await page.content()
            await browser.close()

        soup = BeautifulSoup(html, "html.parser")
        story_links = soup.select("section.story-wrapper a[href]")

        urls = []
        for tag in story_links:
            href = tag["href"]
            if href.startswith("https://www.nytimes.com"):
                urls.append(href)

        print(f"📰 Found {len(urls)} candidate article URLs. Processing up to 5...\n")
        for url in urls[:5]:
            await extract_article_data(url)

    except Exception as e:
        print(f"❌ Error scraping NYTimes homepage: {e}")
