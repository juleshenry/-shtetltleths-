from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time

BASE_URL = "https://juleshenry.github.io"
BLOG_URL = "https://juleshenry.github.io/blog/"

def fetch(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_blog_index(html: str):
    soup = BeautifulSoup(html, "html.parser")
    posts = []
    ul_posts = soup.find("ul", class_="posts")
    if ul_posts:
        for li in ul_posts.find_all("li"):
            date_span = li.find("span")
            if not date_span:
                raise ValueError(f"Could not find date span for a post in {BLOG_URL}")
            date = date_span.get_text(strip=True)
            link = li.find("a", href=True)
            if link and isinstance(link["href"], str):
                href = link["href"]
                title = link.get_text(strip=True)
                absolute_url = urljoin(BASE_URL, href)
                posts.append({
                    "title": title,
                    "url": absolute_url,
                    "date": date
                })
    return posts

def parse_post_content(html: str):
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("section", id="main_content")
    if not main:
        main = soup.find("article") or soup.body

    if main:
        # Remove script, style, header, footer
        for tag in main.find_all(["script", "style", "header", "footer"]):
            tag.decompose()
        
        text = main.get_text(separator="\n", strip=True)
        return text
    return ""

def scrape_and_save(limit=None):
    print(f"Fetching blog index from {BLOG_URL}...")
    index_html = fetch(BLOG_URL)
    posts = parse_blog_index(index_html)
    if limit:
        posts = posts[:limit]
    print(f"Found {len(posts)} posts.")

    all_data = []
    for i, post in enumerate(posts):
        print(f"[{i+1}/{len(posts)}] Fetching {post['url']}...")
        try:
            html = fetch(post["url"])
            content = parse_post_content(html)
            all_data.append({
                "title": post["title"],
                "post": content,
                "timestamp": post["date"]
            })
        except Exception as e:
            print(f"Failed to fetch {post['url']}: {e}")
        time.sleep(1)

    output_file = "juleshenry_posts.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "post", "timestamp"])
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"Saved {len(all_data)} posts to {output_file}")

if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    scrape_and_save(limit=limit)
