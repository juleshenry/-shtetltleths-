import os
from scrape import parse_blog_file
from o_o import shttl as __ot


# fmt: off
__ss=lambda s: (k:=s.strip()).isalpha() or k=='_'
__mz__="""'flesch_kincaid','flesch','gunning_fog','coleman_liau','dale_chall','ari','linsear_write','smog','spache' """
# fmt: on


def zoo_calc(txt):
    return {
        uuy: __ot(uuy, txt)
        for uuy in filter(lambda s: s.replace("'", ""), __mz__.split(","))
    }

if __name__ == "__main__":
    output_dir = "scottaaronson_blog_data"
    go = False 
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith(".txt"):
            filepath = os.path.join(output_dir, filename)
            if 'scottaaronson_blog_2023_10.txt' in filename:
                go = True 
            if not go:
                continue
            print(f"Parsing THE WHOLE MONTH AS ~~!!!@@@@@@{filepath}")
            print("*" * 100)
            for k, v in parse_blog_file(filepath, True, zoo_calc).items():
                print(f"\n$$$$$$$Title: {k}")
                for uuu, iii in v.items():
                    print(uuu, iii)


""""


# _txt = '. '.join([("AIDS banana balls at once commit action and "*12 + " and many, many more")for _ in range(30)])
# if__name__ee0l__main__l0(_txt)
# s_s_s = scrape_blog()
# """