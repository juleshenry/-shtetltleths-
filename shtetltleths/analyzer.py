import os
import json
from .metrics import calculate_all_metrics

def write_to_json(json_dict, json_file_path):
    """
    Appends a dictionary to a JSON list in a file.
    """
    data = []
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
                
    data.append(json_dict)
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def parse_blog_file(filepath):
    """
    Parses a blog archive text file and extracts individual posts and their metrics.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    posts_raw = content.split("=" * 80)
    post_stats_list = []
    
    for post_raw in posts_raw:
        post_raw = post_raw.strip()
        if not post_raw:
            continue
            
        try:
            title = post_raw.split("TITLE:")[1].split("URL:")[0].strip()
            url_part = post_raw.split("URL:")[1].split("CONTENT:")[0].strip()
            
            # Handle optional DATE field if present in the URL part
            if "DATE:" in url_part:
                url = url_part.split("DATE:")[0].strip()
                date = url_part.split("DATE:")[1].strip()
            else:
                url = url_part
                date = "Unknown"
                
            content = post_raw.split("CONTENT:")[1].strip()
            
            if not any(c.isalpha() for c in content[:100]):
                continue
                
            post_data = {
                "title": title,
                "url": url,
                "content": content
            }
            
            post_data.update(calculate_all_metrics(content))
            post_stats_list.append(post_data)
        except (IndexError, ValueError):
            continue
            
    return post_stats_list

def analyze_all_archives(source_dir="scottaaronson_blog_data", output_file="shtetloptimized_stats.json"):
    """
    Processes all archive files in the source directory and saves results to a JSON file.
    """
    if os.path.exists(output_file):
        os.remove(output_file)
        
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    files = sorted([f for f in os.listdir(source_dir) if f.endswith(".txt")])
    
    for filename in files:
        filepath = os.path.join(source_dir, filename)
        print(f"Analyzing {filepath}...")
        date_str = filename.replace("scottaaronson_blog_", "").replace(".txt", "")
        post_stats = parse_blog_file(filepath)
        
        result_entry = {
            "date": date_str,
            "stat_array": post_stats
        }
        write_to_json(result_entry, output_file)
