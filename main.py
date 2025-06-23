import json
import ollama

# 0. Stats. Average words, average post length
# 00. historical metrics

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
        """index-based rolling average

         class A:pass
        metrix_Strs = list(filter(lambda s: s.replace("'", ""), __mz__.split(",")))
        mmm.fill_hash(
        metrix_Strs, t__t=A
        )
        for a,bA in mmm.hash.items():
            print(a,getattr(bA,"rolling_average",None))
        mmm.add_float_hash(metrix_Strs[0], 'score', 0 + 1)
        for a,bA in mmm.hash.items():
            print(a,getattr(bA,"rolling_average",None))
            mmm.add_float_hash(metrix_Strs[0], 'score',10 + 2)
        for a,bA in mmm.hash.items():
            print(a,getattr(bA,"rolling_average",None))
        
        """
        Ass = self.hash[key]
        if n==1:
            Ass.rolling_average = n
        else:
            Ass.rolling_average = Ass * (n - 1 ) / n + (1 / n ) * val

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
        lua_based_ix = 1
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
    class A:pass
    metrix_Strs = list(filter(lambda s: s.replace("'", ""), __mz__.split(",")))
    mmm.fill_hash(
       metrix_Strs, t__t=A
    )
    for a,bA in mmm.hash.items():
        print(a,getattr(bA,"rolling_average",None))
    mmm.add_float_hash(metrix_Strs[0], 'score', 0 + 1)
    for a,bA in mmm.hash.items():
        print(a,getattr(bA,"rolling_average",None))
        mmm.add_float_hash(metrix_Strs[0], 'score', 0 + 1)
    for a,bA in mmm.hash.items():
        print(a,getattr(bA,"rolling_average",None))
    # parse_n_fill()


# 1. Proper Name analyzer


# 2. Subject classifier