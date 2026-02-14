import requests
from bs4 import BeautifulSoup
import re
import time
import os
from datetime import datetime
import pandas as pd

def get_blog_content(url, go=True):
    """
    Fetches blog posts from a specific month's archive URL.
    
    Args:
        url (str): The URL of the monthly archive (e.g., https://scottaaronson.blog/?m=202304).
        go (bool): A flag to enable/disable fetching.
        
    Returns:
        list: A list of dictionaries containing title, content, and url for each post.
    """
    if not go:
        return None
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, "html.parser")
        # Find all blog posts on the page - they are usually in div with class "post"
        posts = soup.find_all("div", class_="post")
        results = []
        
        for post in posts:
            # Extract the title from h3 tag
            title_element = post.find("h3")
            title = (
                title_element.get_text().strip() if title_element else "No title found"
            )
            
            # Extract the content from div with class "entry"
            content_div = post.find("div", class_="entry")
            if content_div:
                paragraphs = content_div.find_all("p")
                paragraph_texts = [p.get_text().strip() for p in paragraphs]
                content = "\n\n".join(paragraph_texts)
            else:
                content = "No content found"
                
            results.append({"title": title, "content": content, "url": url})
        return results
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None

def generate_month_urls(start_year=2005, start_month=10, end_year=2025, end_month=3):
    """
    Generates URLs for the blog's monthly archives from start date to end date.
    
    Format: https://scottaaronson.blog/?m=YYYYMM
    """
    urls = []
    current_date = datetime(start_year, start_month, 1)
    end_date = datetime(end_year, end_month, 1)
    
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        url = f"https://scottaaronson.blog/?m={year}{month:02d}"
        urls.append(url)
        
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)
    return urls

def scrape_blog(output_dir="scottaaronson_blog_data"):
    """
    Scrapes the entire blog archive and saves monthly data to text files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    urls = generate_month_urls()
    all_posts_data = []
    
    for url in urls:
        print(f"Processing {url}")
        match = re.search(r"\?m=(\d{4})(\d{2})", url)
        if not match:
            continue
            
        year, month = match.groups()
        filename = os.path.join(output_dir, f"scottaaronson_blog_{year}_{month}.txt")
        
        if os.path.exists(filename):
            print(f"Already scraped {url}, skipping")
            continue
            
        posts = get_blog_content(url)
        if posts:
            with open(filename, "w", encoding="utf-8") as f:
                for post in posts:
                    f.write(f"TITLE: {post['title']}\n")
                    f.write(f"URL: {post['url']}\n")
                    f.write("CONTENT:\n")
                    f.write(post["content"])
                    f.write("\n\n" + "=" * 80 + "\n\n")
                    
                    all_posts_data.append({
                        "title": post["title"],
                        "post": post["content"]
                    })
            print(f"Saved {len(posts)} posts from {url}")
            
        # Respectful delay to avoid overwhelming the server
        time.sleep(1)
        
    df = pd.DataFrame(all_posts_data)
    print(f"Scraping complete. Total posts scraped: {len(df)}")
    return df

if __name__ == "__main__":
    # To run the scraper, uncomment the line below:
    # scrape_blog()
    print("Blog scraper module loaded. Run scrape_blog() to start scraping.")
