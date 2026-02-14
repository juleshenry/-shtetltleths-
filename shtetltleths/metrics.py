from readability import Readability

class MetricsTracker:
    """
    Tracks rolling averages and historical data for various metrics.
    """
    def __init__(self):
        self.averages = {}
        self.counts = {}
        self.history = {}

    def initialize_metrics(self, metric_names):
        for name in metric_names:
            self.averages[name] = 0.0
            self.counts[name] = 0
            self.history[name] = []

    def add_score(self, metric_name, score):
        if metric_name not in self.averages:
            self.averages[metric_name] = 0.0
            self.counts[metric_name] = 0
            self.history[metric_name] = []

        self.counts[metric_name] += 1
        n = self.counts[metric_name]
        self.averages[metric_name] = (self.averages[metric_name] * (n - 1) / n) + (score / n)
        self.history[metric_name].append(score)

def get_readability_metrics(metric_name, text):
    """
    Calculates a specific readability metric for the given text.
    """
    # Most metrics in py-readability-metrics require 100 words
    if len(text.split()) < 100:
        return {"error": "Text too short (min 100 words)"}
        
    text += ". "
    try:
        r = Readability(text)
        clean_metric = "".join(filter(lambda c: c.isalnum() or c == "_", metric_name)).strip()
        metric_result = getattr(r, clean_metric)()
        return {
            s: getattr(metric_result, s, None)
            for s in ["grade_level", "grade_levels", "ease", "score"]
        }
    except Exception as e:
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
