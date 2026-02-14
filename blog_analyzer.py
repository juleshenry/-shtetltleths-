import os
import json
import ollama
from readability import Readability

def nlp_classify(text):
    """
    Categorizes the blog post into major topics using the phi3 model via Ollama.
    """
    prompt = (
        "Categorize the following blog post into its major topics. "
        "List the main themes or subjects discussed:\n\n"
        f"{text}\n\n"
        "Return a list of topics."
    )
    try:
        response = ollama.chat(model="phi3", messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]
    except Exception as e:
        return f"Error classifying text: {e}"

def get_readability_metrics(metric_name, text):
    """
    Calculates a specific readability metric for the given text.
    
    Args:
        metric_name (str): The name of the readability metric (e.g., 'flesch_kincaid').
        text (str): The text to analyze.
        
    Returns:
        dict: A dictionary containing the score and related info, or an error message.
    """
    # Ensure text is long enough and ends with punctuation
    if len(text.strip()) < 10:
        return {"error": "Text too short for analysis"}
        
    text += ". "
    r = Readability(text)
    
    # Clean metric name to match readability library methods
    clean_metric = "".join(filter(lambda c: c.isalnum() or c == "_", metric_name)).strip()
    
    try:
        metric_result = getattr(r, clean_metric)()
        return {
            s: getattr(metric_result, s, None)
            for s in ["grade_level", "grade_levels", "ease", "score"]
        }
    except Exception as e:
        # Return the last line of the exception message
        return {"error": str(e).split("\n")[-1]}

def calculate_all_metrics(text):
    """
    Calculates all supported readability metrics for the given text.
    """
    metrics_to_calculate = [
        "flesch_kincaid", "flesch", "gunning_fog", "coleman_liau", 
        "dale_chall", "ari", "linsear_write", "smog", "spache"
    ]
    
    results = {}
    for metric in metrics_to_calculate:
        results[metric] = get_readability_metrics(metric, text)
    return results

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
        
    # Split by the separator used in blog_scraper.py
    posts_raw = content.split("=" * 80)
    post_stats_list = []
    
    for post_raw in posts_raw:
        post_raw = post_raw.strip()
        if not post_raw:
            continue
            
        try:
            # Extract metadata and content
            # These splits depend on the format in blog_scraper.py
            title = post_raw.split("TITLE:")[1].split("URL:")[0].strip()
            url = post_raw.split("URL:")[1].split("CONTENT:")[0].strip()
            content = post_raw.split("CONTENT:")[1].strip()
            
            # Basic validation: check if it contains actual text
            if not any(c.isalpha() for c in content[:100]):
                continue
                
            post_data = {
                "title": title,
                "url": url,
                "content": content
            }
            
            # Add readability metrics
            post_data.update(calculate_all_metrics(content))
            post_stats_list.append(post_data)
        except (IndexError, ValueError) as e:
            print(f"Error parsing a post in {filepath}: {e}")
            continue
            
    return post_stats_list

def analyze_all_archives(source_dir="scottaaronson_blog_data", output_file="shtetloptimized_stats.json"):
    """
    Processes all archive files in the source directory and saves results to a JSON file.
    """
    # Remove existing output file to start fresh if needed, 
    # or just let write_to_json append. 
    # For a full reorganization, maybe we want to start fresh.
    if os.path.exists(output_file):
        os.remove(output_file)
        
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    files = sorted([f for f in os.listdir(source_dir) if f.endswith(".txt")])
    
    for filename in files:
        filepath = os.path.join(source_dir, filename)
        print(f"Analyzing {filepath}...")
        
        # Extract date from filename (scottaaronson_blog_YYYY_MM.txt)
        date_str = filename.replace("scottaaronson_blog_", "").replace(".txt", "")
        
        post_stats = parse_blog_file(filepath)
        
        result_entry = {
            "date": date_str,
            "stat_array": post_stats
        }
        
        write_to_json(result_entry, output_file)

if __name__ == "__main__":
    analyze_all_archives()
