from playwright.sync_api import sync_playwright
import time
import os

USER_DATA_DIR = os.path.join(os.getcwd(), "x_user_data")

def find_posts(title: str):
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800},
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        print("🌐 Navigating to X.com")
        page.goto("https://x.com/explore", timeout=60000)

        print(f"🔎 Searching for: {title}")
        page.wait_for_selector("input[placeholder='Search']", timeout=10000)
        page.fill("input[placeholder='Search']", title)
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        for _ in range(3):
            page.mouse.wheel(0, 1000)
            time.sleep(2)

        print("📄 Scraping results...")
        tweets = page.query_selector_all("article")
        results = []

        for tweet in tweets:
            try:
                username_elem = tweet.query_selector('[data-testid="User-Name"] span span')
                content_elem = tweet.query_selector('[data-testid="tweetText"]')

                username = username_elem.inner_text().strip() if username_elem else "Unknown"
                content = content_elem.inner_text().strip() if content_elem else ""

                if content:
                    result = {
                        "username": username,
                        "content": content
                    }
                    results.append(result)

                    print(f"\n📝 Tweet {len(results)}:")
                    print(f"User: {username}")
                    print(f"Content:\n{content}")

                if len(results) >= 5:
                    break
            except Exception as e:
                print(f"⚠️ Error processing tweet: {e}")
                continue

        browser.close()
        return results
