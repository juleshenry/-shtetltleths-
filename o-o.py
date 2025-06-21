"""u = "pip install py-readability-metrics"
from readability import Readability

r = Readability(u)

r.flesch_kincaid()
r.flesch()
r.gunning_fog()
r.coleman_liau()
r.dale_chall()
r.ari()
r.linsear_write()
r.smog()
r.spache()
"""

u = "pip install py-readability-metrics"
from readability import Readability


# fmt: off
mz="""'flesch_kincaid','flesch','gunning_fog','coleman_liau','dale_chall','ari','linsear_write','smog','spache' """
ss=lambda s: (k:=s.strip()).isalpha() or k=='_'
# fmt: on

r = Readability(".".join(u + " ".join(mz.split(",")) * 100))
for m in filter(lambda s: s.replace("'", ""), mz.split(",")):
    m = "".join(filter(ss, m))
    print(f"{m}: {getattr(r, m.strip())()}")
