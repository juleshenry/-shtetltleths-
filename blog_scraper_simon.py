import time
import requests
from bs4 import BeautifulSoup
import csv
import sys
from urllib.parse import urljoin
from datetime import datetime

USER_AGENT = "Mozilla/5.0 (compatible; SimonScraper/1.0; +https://simonwillison.net/)"
BASE_URL = "https://simonwillison.net"

def get_soup(url):
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except Exception as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def parse_segments(soup):
    segments = soup.select("div.segment")
    results = []
    
    for segment in segments:
        data_type = segment.get("data-type", "unknown")
        
        # Title and URL extraction
        title = ""
        post_url = ""
        
        if data_type == "entry":
            title_link = segment.select_one("h3 a")
            if title_link:
                title = title_link.get_text(strip=True)
                post_url = urljoin(BASE_URL, title_link["href"])
        elif data_type == "blogmark":
            title_link = segment.select_one("p strong a")
            if title_link:
                title = title_link.get_text(strip=True)
                post_url = urljoin(BASE_URL, title_link["href"])
        elif data_type == "quotation":
            quote_p = segment.select_one("blockquote p")
            if quote_p:
                title = "Quote: " + quote_p.get_text(strip=True)[:100] + "..."
            permalink = segment.select_one("p.date-and-tags a[rel='bookmark']")
            if permalink:
                post_url = urljoin(BASE_URL, permalink["href"])
        elif data_type == "note":
            note_p = segment.select_one("p")
            if note_p:
                title = "Note: " + note_p.get_text(strip=True)[:100] + "..."
            permalink = segment.select_one("p.date-and-tags a[rel='bookmark']")
            if permalink:
                post_url = urljoin(BASE_URL, permalink["href"])

        # Date extraction
        date_str = ""
        prev_h3 = segment.find_previous("h3", class_="blog-mixed-list-year")
        if prev_h3:
            date_str = prev_h3.get_text(strip=True)
            
        time_tag = segment.select_one("p.date-and-tags a[rel='bookmark'], div.entryFooter a:first-child")
        if time_tag:
            time_text = time_tag.get_text(strip=True)
            if ":" in time_text or "am" in time_text.lower() or "pm" in time_text.lower():
                date_str += f" {time_text}"

        # Summary extraction
        content_texts = []
        for elem in segment.children:
            if elem.name in ["p", "blockquote", "div"]:
                # Avoid date-and-tags and entryFooter
                classes = elem.get("class", [])
                if "date-and-tags" not in classes and "entryFooter" not in classes and "card-container" not in classes:
                    content_texts.append(elem.get_text(strip=True))
        
        summary = " ".join(content_texts)

        if not date_str:
            raise ValueError(f"Could not find date for segment: {title}")

        results.append({
            "type": data_type,
            "title": title,
            "url": post_url,
            "date": date_str,
            "summary": summary,
            "timestamp": date_str
        })
    
    return results

def scrape_section(section_name, start_url, writer, limit_pages=None):
    current_url = start_url
    page_num = 1
    
    while current_url:
        print(f"Scraping {section_name} - Page {page_num}...", file=sys.stderr)
        soup = get_soup(current_url)
        if not soup:
            break
            
        items = parse_segments(soup)
        for item in items:
            writer.writerow(item)
        
        print(f"  Found {len(items)} items.", file=sys.stderr)
        
        if limit_pages and page_num >= limit_pages:
            print(f"  Reached limit of {limit_pages} pages.", file=sys.stderr)
            break

        # Check for next page
        next_url = None
        pagination = soup.select_one("div.pagination")
        if pagination:
            for a in pagination.find_all("a"):
                if "next" in a.get_text().lower():
                    next_url = urljoin(current_url, a["href"])
                    break
        
        if not next_url:
            break
            
        current_url = next_url
        page_num += 1
        time.sleep(1)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit-pages", type=int, default=None)
    args = parser.parse_args()
    limit_pages = args.limit_pages

    sections = [
        ("Entries", "https://simonwillison.net/entries/")
    ]
    
    filename = "simonwillison_all_blogs.csv"
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["type", "title", "url", "date", "summary", "timestamp"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for name, url in sections:
            scrape_section(name, url, writer, limit_pages=limit_pages)

    print(f"Done! Full data saved to {filename}")

if __name__ == "__main__":
    main()
