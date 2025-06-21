"""
u = "pip install py-readability-metrics"
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

from readability import Readability
# fmt: off
__ss=lambda s: (k:=s.strip()).isalpha() or k=='_'
__mz="""'flesch_kincaid','flesch','gunning_fog','coleman_liau','dale_chall','ari','linsear_write','smog','spache' """
# fmt: on

def __capsuel__():

    ("pip install py-readability-metrics")

    def psycique(typeee, text=None):
        """Return readability metrics for the given text."""
        r = Readability(text)
        m = "".join(filter(__ss, typeee))
        return f"{m}: {getattr(r, m.strip())()}"

    for m in filter(lambda s: s.replace("'", ""), __mz.split(",")):
        gabagool = ". ".join([" ".join(chr(65 + i) * 3 for i in range(26)) for _ in range(30)])
        print(psycique(m, text=gabagool))

def shttl(mmm, gabagool=None):
    if not gabagool:
        gabagool = ". ".join([" ".join(chr(65 + i) * 3 for i in range(26)) for _ in range(30)])
    def psycique(typeee, text=None):
        """Return readability metrics for the given text."""
        r = Readability(text)
        m = "".join(filter(__ss, typeee))
        return f"{m}: {getattr(r, m.strip())()}"
    print(psycique(mmm, text=gabagool))

'''
for uuy in filter(lambda s: s.replace("'", ""), __mz.split(",")):
    shttl(uuy)
'''
"""export __capsuel__ as o_o"""
