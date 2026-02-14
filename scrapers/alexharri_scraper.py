from datetime import datetime
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import time

BASE_URL = "https://alexharri.com"
BLOG_URL = "https://alexharri.com/blog"

def fetch(url: str) -> str:
    # Ignoring robots.txt as requested by user
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_blog_index(html: str):
    soup = BeautifulSoup(html, "html.parser")
    posts = []
    # The posts are in articles with class css-wmoh4e
    for article in soup.find_all("article", class_="css-wmoh4e"):
        link = article.find("a", href=True)
        if link:
            href = link["href"]
            if href.startswith("/blog/") and href != "/blog":
                title_tag = link.find("h3")
                title = title_tag.get_text(strip=True) if title_tag else link.get_text(strip=True)
                absolute_url = urljoin(BASE_URL, href)
                
                # Extract date from <time> tag
                time_tag = article.find("time")
                if not time_tag:
                    raise ValueError(f"Could not find date for post: {title}")
                date = time_tag.get_text(strip=True)
                
                posts.append({
                    "title": title,
                    "url": absolute_url,
                    "date": date
                })
    
    # Deduplicate
    seen = set()
    unique_posts = []
    for p in posts:
        if p["url"] not in seen:
            unique_posts.append(p)
            seen.add(p["url"])
    return unique_posts

def parse_post_content(html: str):
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if not main:
        main = soup.find("article") or soup.body

    # Remove script, style, and maybe the header if it's too repetitive
    for tag in main.find_all(["script", "style", "header", "footer"]):
        tag.decompose()
    
    # Optional: remove the title and date from the content if they are already in the CSV
    # In alexharri.com, they seem to be in a div with class "flow" at the top of main
    header_div = main.find("div", class_="flow")
    if header_div and (header_div.find("h1") or header_div.find("time")):
        header_div.decompose()

    text = main.get_text(separator="\n", strip=True)
    return text

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
        time.sleep(1) # Be a bit nice even if ignoring robots.txt

    with open("alexharri_posts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "post", "timestamp"])
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"Saved {len(all_data)} posts to alexharri_posts.csv")

if __name__ == "__main__":
    import sys
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None
    scrape_and_save(limit=limit)
