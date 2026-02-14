import subprocess
import sys
import os

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
    cmd4 = [sys.executable, "main.py", "update"]
    if limit:
        cmd4.extend(["--limit", limit])
    run_command(cmd4)

    print("\nAll scrapers completed.")

if __name__ == "__main__":
    main()
