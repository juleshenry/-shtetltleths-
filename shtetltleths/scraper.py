import requests
from bs4 import BeautifulSoup
import re
import time
import os
from datetime import datetime
import pandas as pd

def get_blog_content(url):
    """
    Fetches blog posts from a specific month's archive URL.
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return None
            
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.find_all("div", class_="post")
        results = []
        
        for post in posts:
            title_element = post.find("h3")
            title = (
                title_element.get_text().strip() if title_element else "No title found"
            )
            
            # Extract date from <small> tag after <h3>
            date_element = post.find("small")
            if date_element:
                date_str = date_element.get_text().strip()
            else:
                # Fallback to month/year from URL if date not found in post
                match = re.search(r"\?m=(\d{4})(\d{2})", url)
                if match:
                    year, month = match.groups()
                    date_str = f"{year}-{month}"
                else:
                    date_str = "Unknown Date"
            
            content_div = post.find("div", class_="entry")
            if content_div:
                paragraphs = content_div.find_all("p")
                paragraph_texts = [p.get_text().strip() for p in paragraphs]
                content = "\n\n".join(paragraph_texts)
            else:
                content = "No content found"
                
            results.append({"title": title, "content": content, "url": url, "date": date_str})
        return results
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        return None

def generate_month_urls(start_year=2005, start_month=10, end_year=None, end_month=None):
    """
    Generates URLs for the blog's monthly archives from start date to end date.
    Defaults to current month if end date is not provided.
    """
    if end_year is None or end_month is None:
        now = datetime.now()
        end_year = now.year
        end_month = now.month

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

def scrape_to_files(output_dir="scottaaronson_blog_data", start_year=2005, start_month=10, limit=None):
    """
    Scrapes the blog archive and saves monthly data to text files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    urls = generate_month_urls(start_year=start_year, start_month=start_month)
    all_new_posts = []
    
    for url in urls:
        if limit and len(all_new_posts) >= limit:
            break
            
        match = re.search(r"\?m=(\d{4})(\d{2})", url)
        if not match:
            continue
            
        year, month = match.groups()
        filename = os.path.join(output_dir, f"scottaaronson_blog_{year}_{month}.txt")
        
        # In test mode/limit mode, we might want to re-scrape even if file exists, 
        # or just skip. The user said "redo them all for me".
        # But if the file exists, it skips.
        
        print(f"Processing {url}")
        posts = get_blog_content(url)
        if posts:
            if limit:
                posts = posts[:max(0, limit - len(all_new_posts))]
                
            with open(filename, "w", encoding="utf-8") as f:
                for post in posts:
                    f.write(f"TITLE: {post['title']}\n")
                    f.write(f"URL: {post['url']}\n")
                    f.write(f"DATE: {post['date']}\n")
                    f.write("CONTENT:\n")
                    f.write(post["content"])
                    f.write("\n\n" + "=" * 80 + "\n\n")
                    
                    all_new_posts.append({
                        "title": post["title"],
                        "post": post["content"],
                        "timestamp": post["date"]
                    })
            print(f"Saved {len(posts)} posts from {url}")
            time.sleep(1)
            
    return all_new_posts

def update_csv(csv_path, new_posts):
    """
    Appends only truly new posts to the CSV file based on title and timestamp.
    """
    if not new_posts:
        print("No new posts to add.")
        return
        
    df_new = pd.DataFrame(new_posts)
    
    if os.path.exists(csv_path):
        df_old = pd.read_csv(csv_path)
        # Check for duplicates based on title and timestamp (or date)
        # We rename timestamp to date if it matches or just use title
        
        # Determine the columns to compare
        old_cols = set(df_old.columns)
        new_cols = set(df_new.columns)
        
        # If new_posts has 'timestamp' but old has 'date' or vice versa, handle it
        if 'timestamp' in new_cols and 'date' in old_cols:
            df_new = df_new.rename(columns={'timestamp': 'date'})
        elif 'date' in new_cols and 'timestamp' in old_cols:
            df_new = df_new.rename(columns={'date': 'timestamp'})
            
        # Merge and drop duplicates
        df_combined = pd.concat([df_old, df_new], ignore_index=True)
        
        # Use subset of columns that exist in both for duplicate detection
        subset = ['title']
        if 'timestamp' in df_combined.columns: subset.append('timestamp')
        elif 'date' in df_combined.columns: subset.append('date')
        
        df_final = df_combined.drop_duplicates(subset=subset, keep='first')
        
        added_count = len(df_final) - len(df_old)
        df_final.to_csv(csv_path, index=False)
        print(f"Added {added_count} new posts to {csv_path} (Skipped {len(new_posts) - added_count} duplicates)")
    else:
        df_new.to_csv(csv_path, index=False)
        print(f"Created {csv_path} with {len(new_posts)} posts")
