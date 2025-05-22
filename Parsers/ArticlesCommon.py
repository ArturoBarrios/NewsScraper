import requests

BACKEND_ENDPOINT = "http://localhost:4000/processScrapedNewsArticle"

GraphQL_URL = "http://localhost:4000/graphql"
def send_to_processing_backend(article):
    try:
        response = requests.post(BACKEND_ENDPOINT, json=article)
        print(f"📤 Sent to backend: {article['title']}")
        print("📡 Status Code:", response.status_code)
        print("📬 Response:", response.text)
        return response
    except Exception as e:
        print(f"❌ Error sending article: {e}")
        return None

import requests


def get_parent_articles(limit=5):
    query = """
    query {
      parentArticles {
        id
        title 
        createdAt
        articles {
          id
          title
          url
          content
          date
        }
      }
    }
    """

    response = requests.post(GraphQL_URL, json={"query": query})

    if response.status_code != 200:
        print(f"⚠️ Error fetching parent articles. Status: {response.status_code}")
        return []

    data = response.json()
    articles = data.get("data", {}).get("parentArticles", [])

    print(f"🔎 Found {len(articles)} parent articles")

    return articles[:limit] if limit else articles