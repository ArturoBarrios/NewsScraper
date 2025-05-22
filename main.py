import asyncio
import requests
from scraper import scrape_article_urls_from_homepage
from Parsers.nytimes import scrape_nytimes_homepage
from Parsers.bluesky_scraper import scrape_bluesky_posts
from Parsers.DrudgeReport import scrape_drudge
from Parsers.x import find_posts
from CommonAI.Attention import searchXTweets

GRAPHQL_ENDPOINT = "http://localhost:4000/graphql"
ARTICLE_LIMIT = 3

def send_to_backend(article):
    mutation = """
    mutation CreateArticle($url: String!, $title: String!, $content: String!, $date: String!) {
      createArticle(url: $url, title: $title, content: $content, date: $date) {
        id
        title
      }
    }
    """

    variables = {
        "url": article["url"],
        "title": article["title"],
        "content": article["content"],
        "date": article["date"],
    }

    response = requests.post(
        GRAPHQL_ENDPOINT,
        json={"query": mutation, "variables": variables}
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)


async def main():
    urls = await scrape_article_urls_from_homepage("https://www.nytimes.com")
    print(f"Found {len(urls)} article URLs. Processing the first {ARTICLE_LIMIT}...\n")

    for url in urls[:ARTICLE_LIMIT]:
        article_data = await extract_article_data(url)
        if article_data:
            print("✅ Got article:", article_data["title"])
            send_to_backend(article_data)
        else:
            print("❌ Skipping failed article\n")

if __name__ == "__main__":
    # asyncio.run(main())
    # asyncio.run(scrape_nytimes_homepage()) 
    # asyncio.run(scrape_drudge())
    asyncio.run(searchXTweets())
    # asyncio.run(find_posts("Israel embassy"))
    # asyncio.run(scrape_bluesky_posts())
