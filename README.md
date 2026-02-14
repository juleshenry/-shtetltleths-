# ShtetlTleths Blog Analysis

## Overview
ShtetlTleths is a tool for scraping and analyzing blog posts. It calculates various readability metrics such as Flesch-Kincaid, ARI, and Gunning Fog scores, and tracks lexical diversity and word counts.

## Summary Statistics

The following table summarizes the average readability metrics across different blog sources:

| Source | Posts Analyzed | Flesch-Kincaid Grade | ARI Grade | Gunning Fog Grade | Lexical Diversity | Avg. Word Count |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Alex Harri** | 18 | 9.77 | 9.55 | 12.40 | 0.23 | 3866.50 |
| **Jules Henry** | 28 | 15.51 | 16.31 | 17.78 | 0.46 | 2000.42 |
| **Scott Aaronson** | 12 | 14.11 | 14.59 | 16.63 | 0.67 | 269.00 |

## Visualizations
The analysis generates time-series plots for these metrics, saved as `writing_stats_time.png`.

## Usage

### Install Dependencies
```bash
pip install pandas matplotlib readability-lxml
```

### Run Analysis
To analyze the CSV files and generate statistics:
```bash
python3 analyze_csvs.py
```

To update Scott Aaronson's blog archives and compute detailed metrics:
```bash
python3 main.py update
python3 main.py analyze
```
