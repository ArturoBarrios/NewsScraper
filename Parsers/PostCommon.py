import requests

API_URL = "http://localhost:4000/graphql"

def create_post(username, content, parent_article_id, created_at):
    mutation = """
    mutation CreateXPost($username: String!, $content: String!, $parentArticleId: String!) {
      createXPost(username: $username, content: $content, parentArticleId: $parentArticleId, createdAt: "%s") {
        id
      }
    }
    """ % created_at

    variables = {
        "username": username,
        "content": content,
        "parentArticleId": parent_article_id
    }

    response = requests.post(API_URL, json={"query": mutation, "variables": variables})

    if response.status_code != 200:
        print(f"❌ Failed to create XPost — status {response.status_code}")
        return None

    print(f"✅ Created XPost")
    return response.json()