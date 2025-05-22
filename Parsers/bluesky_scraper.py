from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import requests
from urllib.parse import urlparse, urlunparse
import random   
from .ArticlesCommon import send_to_processing_backend


BACKEND_ENDPOINT = "http://localhost:4000/processScrapedNewsArticle"

async def scrape_bluesky_posts():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://bsky.app/profile/nytimes.com", timeout=60000)

        try:
            await page.wait_for_selector('[data-testid="postText"]', timeout=10000)
        except:
            print("❌ No posts appeared within timeout.")
            await browser.close()
            return

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")
        await browser.close()

        post_blocks = soup.select('[data-testid="postText"]')
        print(f"🔎 Found {len(post_blocks)} posts")

        for i, post in enumerate(post_blocks[:5]):
            text = post.get_text(separator="\n", strip=True)

            # Look for an external article link
            external_link_tag = post.find("a", href=True)
            external_url = None
            if external_link_tag:
                href = external_link_tag["href"]
                if href.startswith("https://nyti.ms") or href.startswith("https://www.nytimes.com"):
                    external_url = href

            if not external_url:
                # fallback to internal post link with unique URL
                post_link_tag = post.find("a", href=True)
                post_href = post_link_tag["href"] if post_link_tag else "/profile/nytimes.com"
                external_url = f"https://bsky.app{post_href}"

            print(f"🧪 Post {i + 1} content preview:\n{text[:150]}...\n")
            print(f"🔗 External URL: {external_url}"     )

            parsed_url = urlparse(external_url)
            unique_url = urlunparse(parsed_url._replace(query="", fragment=""))

            # Optionally, append a random number to make the URL unique
            unique_url = f"{unique_url}?rand={random.randint(100000, 999999)}"

            article = {
                "url": unique_url,
                "title": f"Bluesky Post {i + 1}",
                "content": text,
                "date": "2025-05-19T00:00:00Z",
            }
            send_to_processing_backend(article)
            

