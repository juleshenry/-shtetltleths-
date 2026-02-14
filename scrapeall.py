import subprocess
import sys
import os
import shutil

ERASE_LIST = [
    "simonwillison_all_blogs.csv",
    "scottaaronson_blog_posts.csv",
    "alexharri_posts.csv",
    "juleshenry_posts.csv",
    "scottaaronson_blog_data",
    "scrapers/juleshenry_posts.csv",
    "scrapers/alexharri_posts.csv",
    "shtetloptimized_stats.json",
    "stats_output.txt",
    "writing_stats.png",
    "writing_stats_time.png"
]

def cleanup():
    print("--- Cleaning up existing data ---")
    for item in ERASE_LIST:
        if os.path.isdir(item):
            print(f"Removing directory: {item}")
            shutil.rmtree(item)
        elif os.path.isfile(item):
            print(f"Removing file: {item}")
            os.remove(item)

def run_command(command):
    print(f"Running: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {' '.join(command)}: {e}")

def main():
    test_mode = "--test" in sys.argv
    limit = "5" if test_mode else None
    
    print(f"Starting Scrape All {'(TEST MODE)' if test_mode else ''}")
    
    # Clean up before running
    cleanup()
    
    # 1. Simon Willison
    print("\n--- Scraping Simon Willison ---")
    cmd1 = [sys.executable, "blog_scraper_simon.py"]
    if test_mode:
        cmd1.extend(["--limit-pages", "1"])
    run_command(cmd1)
    
    # 2. Jules Henry
    print("\n--- Scraping Jules Henry ---")
    cmd2 = [sys.executable, "scrapers/juleshenry_scraper.py"]
    if limit:
        cmd2.append(limit)
    run_command(cmd2)
    
    # 3. Alex Harri
    print("\n--- Scraping Alex Harri ---")
    cmd3 = [sys.executable, "scrapers/alexharri_scraper.py"]
    if limit:
        cmd3.append(limit)
    run_command(cmd3)
    
    # 4. Scott Aaronson (ShtetlTleths)
    print("\n--- Scraping Scott Aaronson ---")
    # Using 'update' command which scrapes and then updates CSV
    cmd4 = [sys.executable, "main.py", "update"]
    if limit:
        cmd4.extend(["--limit", limit])
    run_command(cmd4)

    # 5. Analysis
    print("\n--- Running Analysis ---")
    run_command([sys.executable, "analyze_csvs.py"])

    print("\nAll scrapers and analysis completed.")

if __name__ == "__main__":
    main()
