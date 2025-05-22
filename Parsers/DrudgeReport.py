from bs4 import BeautifulSoup
import requests

from .ArticlesCommon import send_to_processing_backend
from datetime import datetime

async def scrape_drudge():
    url = "https://www.drudgereport.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    anchors = soup.find_all("a", href=True)

    headlines = []
    for tag in anchors:
        text = tag.get_text(strip=True)
        href = tag["href"]
        if text and href.startswith("http"):
            headlines.append((text, href))

    print(f"🔎 Found {len(headlines)} headlines on Drudge Report")
    date = datetime.utcnow().isoformat() + "Z"

    for title, href in headlines[:5]:
        article = {
            "url": href,
            "title": title,
            "date": date,
            "content": title  # You can replace this with full content later if scraped
        }
        send_to_processing_backend(article)

    return headlines
