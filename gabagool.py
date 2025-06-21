import os
from scrape import parse_blog_file
from o_o import shttl as __ot


# fmt: off
__ss=lambda s: (k:=s.strip()).isalpha() or k=='_'
__mz__="""'flesch_kincaid','flesch','gunning_fog','coleman_liau','dale_chall','ari','linsear_write','smog','spache' """
# fmt: on
def if__name__ee0l__main__l0(txt):
    for uuy in filter(lambda s: s.replace("'", ""), __mz__.split(",")):
        print(uuy)
        __ot(uuy, txt)


# _txt = '. '.join([("AIDS banana balls at once commit action and "*12 + " and many, many more")for _ in range(30)])
# if__name__ee0l__main__l0(_txt)

if __name__ == "__main__":
    # s = scrape_blog()
    # Test with a sample file
    print = lambda *a: a
    output_dir = "scottaaronson_blog_data"
    for filename in os.listdir(output_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(output_dir, filename)
            print(f"Parsing THE WHOLE MONTH AS ~~!!!@@@@@@{filepath}")
            posts_dict = parse_blog_file(filepath, True, if__name__ee0l__main__l0)
            print(f"Extracted {len(posts_dict)} posts from {filename}")
            for title, content in posts_dict.items():
                print(f"\nTitle: {title}")
                print(f"Content length: {len(content)} characters")
parse_blog_file
# parse_blog_file()
