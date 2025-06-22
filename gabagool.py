import os
from scrape import parse_blog_file
from o_o import lexical_analisis

# fmt: off
__ss=lambda s: (k:=s.strip()).isalpha() or k=='_'
__mz__="""flesch_kincaid,flesch,gunning_fog,coleman_liau,dale_chall,ari,linsear_write,smog,spache"""
# fmt: on


def zoo_calc(txt):
    e = {}
    for lex_tech in filter(lambda s: s.replace("'", ""), __mz__.split(",")):
        e[lex_tech] = lexical_analisis(lex_tech, txt)
    return e


if __name__ == "__main__":
    output_dir = "scottaaronson_blog_data"
    go = False
    for filename in sorted(os.listdir(output_dir)):
        if filename.endswith(".txt"):
            filepath = os.path.join(output_dir, filename)
            if "scottaaronson_blog_2011_01.txt" in filename or True:
                go = True
            if not go:
                continue
            print(f"Parsing THE WHOLE MONTH AS ~~!!!@@@@@@{filepath}")
            # print("*" * 100)
            stat_dict_arr = parse_blog_file(filepath, True, zoo_calc)
            for stat_dict in stat_dict_arr:
                for k, v in stat_dict.items():
                    print(f"{k} ::: {'~' if k=='content' else v}")


""""


# _txt = '. '.join([("AIDS banana balls at once commit action and "*12 + " and many, many more")for _ in range(30)])
# if__name__ee0l__main__l0(_txt)
# s_s_s = scrape_blog()
# """
