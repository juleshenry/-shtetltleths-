import json
import ollama

# 0. Stats. Average words, average post length
# 00. historical metrics
# 1. Proper Name analyzer


# 2. Subject classifier
def nlp_classify(text):
    prompt = (
        "Categorize the following blog post into its major topics. "
        "List the main themes or subjects discussed:\n\n"
        f"{text}\n\n"
        "Return a list of topics."
    )
    response = ollama.chat(model="phi3", messages=[{"role": "user", "content": prompt}])
    # Extract topics from response
    return response["message"]["content"]


class MetricScore:

    def __init__(self, metr_str="¿", score=None):
        self.score = score
        self.metric_str = metr_str


class Metrixoid:

    # running tally box
    def __init__(self, hash={}):
        self.hash = hash

    def fill_hash(self, list_strs, t__t=None):
        self.hash = {ls: t__t() if t__t else t__t for ls in list_strs}

    def add_float_hash(self, key, val, n):
        ss = self.hash[key]
        self.hash[key] = ss * (n-1) / n + (1 /n ) * val

def parse_n_fill():
    """
    if __name__ == '__main__':
        with open('shtetloptimized_stats.json')as f:
            data = json.load(f)
            for entry in data[:5]:
                print(entry["date"])
                for stat in entry["stat_array"]:
                    # if ('error' in stat.values().keys())
                    for v,k in stat.items():
                        print(v)
                        print(str(k[:40]).strip()+'... ~~~' if type(k)==str else k)
                        print()
                    print()
                    print()
    """
    with open("shtetloptimized_stats.json") as f:
        data = json.load(f)
        for entry in data[:5]:
            print(entry["date"])
            for stat in entry["stat_array"]:
                # if ('error' in stat.values().keys())
                for v, k in stat.items():
                    print(v)
                    print(str(k[:40]).strip() + "... ~~~" if type(k) == str else k)
                    print()


if __name__ == "__main__":
    __mz__ = """flesch_kincaid,flesch,gunning_fog,coleman_liau,dale_chall,ari,linsear_write,smog,spache"""
    mmm = Metrixoid({})
    mmm.fill_hash(
        list(filter(lambda s: s.replace("'", ""), __mz__.split(","))), t__t=list
    )
    print(mmm.hash)
    parse_n_fill()
