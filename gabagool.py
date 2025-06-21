from scrape import parse_blog_file
from o_o import shttl as __ot
# fmt: off
__ss=lambda s: (k:=s.strip()).isalpha() or k=='_'
__mz__="""'flesch_kincaid','flesch','gunning_fog','coleman_liau','dale_chall','ari','linsear_write','smog','spache' """
# fmt: on
if __name__ == "__main__":
    for uuy in filter(lambda s: s.replace("'", ""), __mz__.split(",")):
        __ot(uuy)

# parse_blog_file()