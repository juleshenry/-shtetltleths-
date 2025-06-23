import os
import json
from readability import Readability


def alpha_underscore(s):
    return (k := s.strip()).isalpha() or k == "_"


def lexical_analisis(metric, text):
    """Return readability metrics for the given text."""
    text += ". "
    r = Readability(text)
    purify_metric = "".join(filter(alpha_underscore, metric))
    try:
        izzy = getattr(r, purify_metric.strip())()
        return {
            s: getattr(izzy, s, None)
            for s in ["grade_level", "grade_levels", "ease", "score"]
        }
    except Exception as ee:
        return {"error": str(ee).split("\n")[-1]}


def zoo_calc(txt):
    e = {}
    # fmt: off
    __mz__="""flesch_kincaid,flesch,gunning_fog,coleman_liau,dale_chall,ari,linsear_write,smog,spache"""
    # fmt: on
    for lex_tech in filter(lambda s: s.replace("'", ""), __mz__.split(",")):
        e[lex_tech] = lexical_analisis(lex_tech, txt)
    return e


def write_to_json(json_dict, json_file_path):
    # appends to json file
    data = []
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    data.append(json_dict)
    with open(json_file_path, "w") as f:
        json.dump(data, f, indent=2)


def parse_blog_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        file_blob = f.read()
    posts = file_blob.split("=" * 80)
    post_stats_arr = []
    for post in posts:
        if not post.strip():
            continue
        post_stats = {}

        title_match = post.split("TITLE:")[1].split("URL:")[0]
        url_match = post.split("URL: ")[1].split("CONTENT:")[0]
        content_match = post.split("CONTENT:")[1]

        post_stats["title"] = title_match
        post_stats["url"] = url_match
        post_stats["content"] = content_match
        if not any(o.isalpha() for o in post_stats["content"][:64]):
            continue
        post_stats.update(**zoo_calc(content_match))
        post_stats_arr.append(post_stats)

    return post_stats_arr


if __name__ == "__main__":
    scraped_source = "scottaaronson_blog_data"
    output_file_name = "shtetloptimized_stats.json"
    for filename in sorted(os.listdir(scraped_source)):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(scraped_source, filename)
        print(f"Parsing THE WHOLE MONTH AS ~~!!!@@@@@@{filepath}")
        stat_dict_arr = parse_blog_file(filepath)
        out_json = {
            "date": filename.split("blog_")[1].split(".")[0],
            "stat_array": stat_dict_arr,
        }
        write_to_json(out_json, output_file_name)

# _txt = '. '.join([("AIDS banana balls at once commit action and "*12 + " and many, many more")for _ in range(30)])
# if__name__ee0l__main__l0(_txt)
# s_s_s = scrape_blog()
# """
