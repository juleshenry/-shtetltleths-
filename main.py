import json
import ollama
import numpy as np
import calendar

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

    def add_float_hash(self, metric, metric_attr, value, n):
        """index-based rolling average
        key of the hash map {metric: running_Avg}
        self.hash[key]
        val
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
        # print(metric, metric_attr, value, n)
        if n == 1:
            setattr(self.hash[metric], metric_attr, value)
        else:
            score = getattr(self.hash[metric], metric_attr)
            score *= (n - 1) / n
            setattr(self.hash[metric], metric_attr, score)
            setattr(
                self.hash[metric],
                metric_attr,
                getattr(self.hash[metric], metric_attr) + ((1 / n) * value),
            )
            # print(metric_A)
            # print( getattr(metric_A, metric_attr))
            # print(n,metric_attr)
            # a.rolling_average += ((1 / n) * value)


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
                for metriac, k in stat.items():
                    print(metriac)
                    print(str(k[:40]).strip() + "... ~~~" if type(k) == str else k)
                    print()


docz = """"
if __name__ == "__main__":
    __mz__ = '''flesch_kincaid,flesch,gunning_fog,coleman_liau,dale_chall,ari,linsear_write,smog,spache'''
    mmm = Metrixoid({})

    class A:
        pass

    metrix_Strs = list(filter(lambda s: s.replace("'", ""), __mz__.split(",")))
    mmm.fill_hash(metrix_Strs, t__t=A)

    ex_triplet = (3,6,9,)
    for a, bA in mmm.hash.items():
        if getattr(bA, "score", None):
            print(a, getattr(bA, "score", None))

    metric = "flesch_kincaid"

    mmm.add_float_hash(metric, "score", ex_triplet[0], 0 + 1)
    for a, bA in mmm.hash.items():
        if not getattr(bA, "score", None):
            continue
        print(a, getattr(bA, "score", None))

    mmm.add_float_hash(metrix_Strs[0], "score", ex_triplet[1], 1 + 1)
    for a, bA in mmm.hash.items():
        if not getattr(bA, "score", None):
            continue
        print(a, getattr(bA, "score", None))

    mmm.add_float_hash(metrix_Strs[0], "score", ex_triplet[2], 2 + 1)
    for a, bA in mmm.hash.items():
        if not getattr(bA, "score", None):
            continue
        print(a, getattr(bA, "score", None))
    # parse_n_fill()
"""

docz2 = '''
    __mz__ = """flesch_kincaid,flesch,gunning_fog,coleman_liau,dale_chall,ari,linsear_write,smog,spache"""
    mmm = Metrixoid({})

    class A:
        pass

    metrix_Strs = list(filter(lambda s: s.replace("'", ""), __mz__.split(",")))

    mmm.fill_hash(metrix_Strs, t__t=A)

    for metriac, Ao in mmm.hash.items():
        Ao_score = getattr(Ao, "score", None)
        print(metriac, Ao_score)

    for metriac, Ao in mmm.hash.items():
        Ao_score = getattr(Ao, "score", None)
        mmm.add_float_hash(
            metriac,
            "score",
            *(
                69,
                1,
            ),
        )

    for metriac, Ao in mmm.hash.items():
        Ao_score = getattr(Ao, "score", None)
        print(metriac, Ao_score)

    for metriac, Ao in mmm.hash.items():
        Ao_score = getattr(Ao, "score", None)
        mmm.add_float_hash(
            metriac,
            "score",
            *(
                71,
                2,
            ),
        )

    for metriac, Ao in mmm.hash.items():
        Ao_score = getattr(Ao, "score", None)
        print(metriac, Ao_score)
'''

docz3 = '''
    __mz__ = """flesch_kincaid,flesch,gunning_fog,coleman_liau,dale_chall,ari,linsear_write,smog,spache"""
    mmm = Metrixoid({})
    class A:
        pass

    metrix_Strs = list(filter(lambda s: s.replace("'", ""), __mz__.split(",")))
    mmm.fill_hash(metrix_Strs, t__t=A)
    # for ix, value in zip(range(1, 1 + 10), range(0, 0 + 10)):
    #     for metriac, Ao in mmm.hash.items():
    #         mmm.add_float_hash(metriac, "score", value, ix)
    # for metriac, Ao in mmm.hash.items():
    #     print(metriac, Ao.score)
    list(map(lambda a:print(a.score),mmm.hash.values()))

'''
docz4 = '''
if __name__ == "__main__":
    __mz__ = """flesch_kincaid,flesch,gunning_fog,coleman_liau,dale_chall,ari,linsear_write,smog,spache"""
    mmm = Metrixoid({})

    class A:
        pass

    metrix_Strs = list(filter(lambda s: s.replace("'", ""), __mz__.split(",")))
    mmm.fill_hash(metrix_Strs, t__t=A)
    # for ix, value in zip(range(1, 1 + 10), range(0, 0 + 10)):
    #     for metriac, Ao in mmm.hash.items():
    #         mmm.add_float_hash(metriac, "score", value, ix)
    # for metriac, Ao in mmm.hash.items():
    #     print(metriac, Ao.score)
    metr_hist = Metrixoid({})
    metr_hist.fill_hash(metrix_Strs, t__t=list)
    print("#############")
    with open("shtetloptimized_stats.json") as f:
        data = json.load(f)
        # lua based index
        metr_ix = {m: 1 for m in metrix_Strs}
        for entry in data[:1]:  # data[:1]: ---< edebug...
            print(entry['date'])
            for stat in entry["stat_array"]:
                score = None
                for metric in metrix_Strs:
                    met_score = stat[metric].get("score")
                    if met_score:
                        mmm.add_float_hash(metric, "score", met_score, metr_ix[metric])
                        metr_ix[metric] += 1
                        metr_hist.hash[metric] += ([met_score])
                        if 'smog' == metric:
                            print(stat['content'])
    print(metr_ix)
    print("<3"*8)
    for metriac, Ao in mmm.hash.items():
        print(metriac, Ao.score) # metr_hist.hash[metriac])
'''

if __name__ == "__main__":
    __mz__ = """flesch_kincaid,flesch,gunning_fog,coleman_liau,dale_chall,ari,linsear_write,smog,spache"""
    mmm = Metrixoid({})

    class A:
        pass

    # key:metric, value:A_class
    metrix_Strs = list(filter(lambda s: s.replace("'", ""), __mz__.split(",")))
    mmm.fill_hash(metrix_Strs, t__t=A)

    # {key:metric, value:list[float]}
    metr_hist = Metrixoid({})
    metr_hist.fill_hash(metrix_Strs, t__t=list)

    with open("shtetloptimized_stats.json") as f:
        data = json.load(f)
        metr_ix = {m: 1 for m in metrix_Strs}
        for entry in data:
            for stat in entry["stat_array"]:
                for metric in metrix_Strs:
                    met_score = stat[metric].get("score")
                    if met_score:
                        mmm.add_float_hash(metric, "score", met_score, metr_ix[metric])
                        metr_ix[metric] += 1
                        metr_hist.hash[metric] += [met_score]
                    else:
                        metr_hist.hash[metric] += [
                            0
                        ]  # fill with zeroes if no score for entry
    print(metr_ix)
    print("<3" * 8)
    for metriac, Ao in mmm.hash.items():
        # avg
        # score
        # hash
        print(metriac)
        print(Ao.score)
    # 1/0
    import matplotlib.pyplot as plt

    # Prepare x-axis: one value per month starting Jan 2005
    num_points = len(next(iter(metr_hist.hash.values())))
    months = np.arange(num_points)
    start_year = 2005
    start_month = 10

    # Generate list of month labels
    month_labels = []
    year = start_year
    month = start_month
    for _ in range(num_points):
        month_labels.append(f"{calendar.month_abbr[month]} {year}")
        month += 1
        if month > 12:
            month = 1
            year += 1

    plt.figure(figsize=(14, 8))
    for metriac, score_obj in metr_hist.hash.items():
        if not score_obj:
            continue
        plt.plot(months, score_obj, label=metriac)
        plt.axhline(
            y=mmm.hash[metriac].score,
            color=plt.gca().lines[-1].get_color(),
            linestyle=":",
            linewidth=1,
            alpha=0.5,
        )
        plt.title(f"Shtetl-Optimized :{metriac} :avg({mmm.hash[metriac].score})")
        plt.xlabel("Month (starting October 2005)")
        plt.ylabel("Score")
        plt.legend()
        plt.xticks(
            ticks=np.arange(0, num_points, max(1, num_points // 12)),
            labels=[
                month_labels[i] for i in range(0, num_points, max(1, num_points // 12))
            ],
            rotation=45,
        )
        plt.tight_layout()
        plt.show()

# 1. Proper Name analyzer


# 2. Subject classifier
