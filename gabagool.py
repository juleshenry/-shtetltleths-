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


# _txt = '. '.join([("AIDS banana balls at once commit action and "*12 + " and many, many more")for _ in range(30)])
# if__name__ee0l__main__l0(_txt)

if __name__ == "__main__":
    # s_s_s = scrape_blog()
    # p = print
    output_dir = "scottaaronson_blog_data"
    go = False 
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith(".txt"):
            filepath = os.path.join(output_dir, filename)
            if 'scottaaronson_blog_2008_05.txt' in filename:
                go = True
            if not go:
                return
            print(f"Parsing THE WHOLE MONTH AS ~~!!!@@@@@@{filepath}")
            print("*" * 100)
            for k, v in parse_blog_file(filepath, True, zoo_calc).items():
                print(f"\n$$$$$$$Title: {k}")
                for uuu, iii in v.items():
                    print(uuu, iii)
                # print(f"Content length: {} characters")
                # 1 / 0
            # Uncomment the following lines to print the extracted posts
            # p(f"Extracted {len(posts_dict)} posts from {filename}")
            # for title, content in posts_dict.items():
            #     print(f"\nTitle: {title}")
            #     print(f"Content length: {len(content)} characters")
# parse_blog_file
# parse_blog_file()
