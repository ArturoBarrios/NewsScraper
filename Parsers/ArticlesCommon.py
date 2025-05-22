import requests

BACKEND_ENDPOINT = "http://localhost:4000/processScrapedNewsArticle"

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