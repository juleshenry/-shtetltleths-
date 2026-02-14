import json
import numpy as np
import calendar
import matplotlib.pyplot as plt

class MetricsTracker:
    """
    Tracks rolling averages and historical data for various metrics.
    """
    def __init__(self):
        self.averages = {}  # {metric_name: average_value}
        self.counts = {}    # {metric_name: number_of_entries}
        self.history = {}   # {metric_name: list_of_values}

    def initialize_metrics(self, metric_names):
        """Initializes trackers for the given list of metrics."""
        for name in metric_names:
            self.averages[name] = 0.0
            self.counts[name] = 0
            self.history[name] = []

    def add_score(self, metric_name, score):
        """Adds a new score and updates the rolling average."""
        if metric_name not in self.averages:
            self.averages[metric_name] = 0.0
            self.counts[metric_name] = 0
            self.history[metric_name] = []

        self.counts[metric_name] += 1
        n = self.counts[metric_name]
        
        # Update rolling average: avg_n = avg_{n-1} * (n-1)/n + score/n
        self.averages[metric_name] = (self.averages[metric_name] * (n - 1) / n) + (score / n)
        self.history[metric_name].append(score)

def load_stats(filename="shtetloptimized_stats.json"):
    """Loads stats from the generated JSON file."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename}: {e}")
        return []

def plot_metrics(tracker, metric_names):
    """Plots the historical metrics using matplotlib."""
    if not tracker.history:
        print("No data to plot.")
        return

    # Determine number of points (assuming all metrics have same number of history points)
    # This might vary if some months had no posts, but here we expect one entry per month
    num_points = len(next(iter(tracker.history.values())))
    months_idx = np.arange(num_points)
    
    # Generate month labels starting from Oct 2005
    month_labels = []
    year, month = 2005, 10
    for _ in range(num_points):
        month_labels.append(f"{calendar.month_abbr[month]} {year}")
        month += 1
        if month > 12:
            month = 1
            year += 1

    plt.figure(figsize=(15, 10))
    ncols = 3
    nrows = (len(metric_names) + ncols - 1) // ncols

    for idx, metric in enumerate(metric_names):
        if metric not in tracker.history or not tracker.history[metric]:
            continue
            
        ax = plt.subplot(nrows, ncols, idx + 1)
        ax.plot(months_idx, tracker.history[metric], label="Monthly Score", alpha=0.7)
        
        # Draw average line
        avg = tracker.averages[metric]
        ax.axhline(y=avg, color="red", linestyle=":", linewidth=1.5, label=f"Avg: {avg:.2f}")
        
        ax.set_title(f"{metric.replace('_', ' ').title()}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Score")
        
        # Set ticks for better readability
        tick_spacing = max(1, num_points // 10)
        ax.set_xticks(months_idx[::tick_spacing])
        ax.set_xticklabels([month_labels[i] for i in range(0, num_points, tick_spacing)], 
                           rotation=45, fontsize=8)
        ax.legend(fontsize='small')

    plt.tight_layout()
    plt.show()

def main():
    metric_names = [
        "flesch_kincaid", "flesch", "gunning_fog", "coleman_liau", 
        "dale_chall", "ari", "linsear_write", "smog", "spache"
    ]
    
    tracker = MetricsTracker()
    tracker.initialize_metrics(metric_names)
    
    data = load_stats()
    if not data:
        print("No data found. Please run blog_analyzer.py first.")
        return

    for entry in data:
        # Each entry represents one month
        # We'll calculate the average for the month if there are multiple posts
        month_metrics = {m: [] for m in metric_names}
        
        for post in entry.get("stat_array", []):
            for metric in metric_names:
                score = post.get(metric, {}).get("score")
                if score is not None:
                    month_metrics[metric].append(score)
        
        # Add the monthly average to our tracker
        for metric in metric_names:
            if month_metrics[metric]:
                monthly_avg = sum(month_metrics[metric]) / len(month_metrics[metric])
                tracker.add_score(metric, monthly_avg)
            else:
                tracker.add_score(metric, 0.0) # Or handle missing data differently

    print("Metrics Analysis Complete.")
    for metric in metric_names:
        print(f"{metric:15}: Average Score = {tracker.averages[metric]:.2f}")
        
    plot_metrics(tracker, metric_names)

if __name__ == "__main__":
    main()
