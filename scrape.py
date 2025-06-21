import requests
from bs4 import BeautifulSoup
import re
import time
import os
from datetime import datetime, timedelta
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize


def get_blog_content(url):
    """
    Scrapes a specific blog page and extracts titles and paragraph text
    """
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}, status code: {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all blog posts on the page
        posts = soup.find_all("div", class_="post")

        results = []
        for post in posts:
            # Extract the title
            title_element = post.find("h3")
            title = (
                title_element.get_text().strip() if title_element else "No title found"
            )

            # Extract paragraphs - looking for all p tags within the post content
            content_div = post.find("div", class_="entry")

            if content_div:
                paragraphs = content_div.find_all("p")
                paragraph_texts = [p.get_text().strip() for p in paragraphs]

                # Combine all paragraph texts
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
    Generates URLs for the blog's monthly archives from start_year/month to end_year/month
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

        # Move to next month
        if month == 12:
            current_date = datetime(year + 1, 1, 1)
        else:
            current_date = datetime(year, month + 1, 1)

    return urls


def scrape_blog():
    """
    Main function to scrape Scott Aaronson's blog
    """
    # Create directory for saving results
    output_dir = "scottaaronson_blog_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate URLs for all months from Jan 2011 to the current date
    urls = generate_month_urls()

    all_posts = pd.DataFrame(columns=["title", "post"])
    # Process each monthly archive
    for url in urls:
        print(f"Processing {url}")

        # Extract year and month from URL for filename
        match = re.search(r"\?m=(\d{4})(\d{2})", url)
        if match:
            year, month = match.groups()
            filename = f"{output_dir}/scottaaronson_blog_{year}_{month}.txt"

            # Check if we've already scraped this month
            if os.path.exists(filename):
                print(f"Already scraped {url}, skipping")
                continue

            posts = get_blog_content(url)

            if posts:
                # Save this month's posts to a file
                with open(filename, "w", encoding="utf-8") as f:
                    for post in posts:
                        f.write(f"TITLE: {post['title']}\n")
                        f.write(f"URL: {post['url']}\n")
                        f.write("CONTENT:\n")
                        f.write(post["content"])
                        f.write("\n\n" + "=" * 80 + "\n\n")
                        # Add posts to the DataFrame
                        all_posts = pd.concat(
                            [
                                all_posts,
                                pd.DataFrame(
                                    {
                                        "title": [post["title"]],
                                        "post": [post["content"]],
                                    }
                                ),
                            ],
                            ignore_index=True,
                        )
                print(f"Saved {len(posts)} posts from {url}")

            # Be nice to the server
            time.sleep(2)

    print(f"Scraping complete. Total posts scraped: {len(all_posts)}")
    return all_posts


def parse_blog_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by multiple equal signs to separate posts
    posts = content.split("=" * 80)
    blog_dict = {}

    for post in posts:
        if post.strip():
            # Extract title and content
            title_match = post.split('TITLE: ')[1].split('URL: ')[0]
            print('tit',title_match)
            url_match = post.split("URL: ")[1].split("CONTENT:")[0]
            print('url',url_match)
            # print(url_match)
            content_match = post.split("CONTENT:")[1]
            print('~~~~',)
            print(content_match[:32] + f"...{len(content_match[32:-32])}%%%L8R$..." + content_match[-32:])
            print('~~~~',)
            
            1/0
    return blog_dict


def test_parse_blog_file():
    """Test the parse_blog_file function with a sample file"""
    output_dir = "scottaaronson_blog_data"
    sample_file = f"{output_dir}/scottaaronson_blog_2023_04.txt"
    if os.path.exists(sample_file):
        posts_dict = parse_blog_file(sample_file)
        print("Extracted posts:", len(posts_dict))
        for title in posts_dict:
            print(f"\nTitle: {title}")
            print(f"Content length: {len(posts_dict[title])} characters")


if __name__ == "__main__":
    # s = scrape_blog()
    # Test with a sample file
    output_dir = "scottaaronson_blog_data"
    for filename in os.listdir(output_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(output_dir, filename)
            print(f"Parsing {filepath}")
            posts_dict = parse_blog_file(filepath)
            print(f"Extracted {len(posts_dict)} posts from {filename}")
            for title, content in posts_dict.items():
                print(f"\nTitle: {title}")
                print(f"Content length: {len(content)} characters")
