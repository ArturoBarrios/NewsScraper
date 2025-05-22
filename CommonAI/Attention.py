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
from Parsers.ArticlesCommon import get_parent_articles
from Parsers.PostCommon import create_post

API_URL = "http://localhost:4000/graphql"  # change this if deployed

async def searchXTweets(limit=5):
    
    parentArticlesSelected = get_parent_articles(limit)

    for parent in parentArticlesSelected:
        title = parent.get("title", "").strip().strip('"').strip("'")
        parent_id = parent.get("id")

        if not title or not parent_id:
            continue

        print(f"\n🧠 Looking up social posts for: {title}")
        posts = await asyncio.to_thread(find_posts, title)

        for i, post in enumerate(posts, 1):
            username = post.get("username", "").strip()
            content = post.get("content", "").strip()

            if not username or not content:
                continue

            print(f"\n📣 Creating XPost {i}:")
            print(f"User: {username}")
            print(f"Content: {content}")


            post_response = create_post(username, content, parent_id, "")