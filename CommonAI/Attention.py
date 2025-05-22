# essentially aims to see the whole picture of some parent article
# need to think about how to implement this in the frontend
# get parent articles with articles attached
# idk what this file really represents, context maybe
# find stories to remove, by paying attention to what doesn't matter

# number of articles in parent

# ideas around social media
# maybe attach  social media posts to articles


#if you have posts around an article, aimed at true understanding
#what do people really think
#you could start thinking about giving weight to users
#you could add weight to users to you Attention.py script 

import requests
import asyncio

from Parsers.x import find_posts

API_URL = "http://localhost:4000/graphql"  # change this if deployed

async def get_parent_articles_with_articles(limit=5):
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

    response = requests.post(API_URL, json={"query": query})

    if response.status_code != 200:
        print(f"⚠️ Error fetching parent articles. Status: {response.status_code}")
        return []

    data = response.json()
    articles = data.get("data", {}).get("parentArticles", [])

    print(f"🔎 Found {len(articles)} parent articles")

    selected = articles[:limit] if limit else articles

    for parent in selected:
        title = parent.get("title", "").strip().strip('"').strip("'")
        if not title:
            continue

        print(f"\n🧠 Looking up social posts for: {title}")
        posts = await asyncio.to_thread(find_posts, title)

        for i, post in enumerate(posts, 1):
            print(f"\n📣 Post {i} from X:")
            print(f"User: {post.get('username')}")
            print(f"Content: {post.get('content')}")

    return selected



