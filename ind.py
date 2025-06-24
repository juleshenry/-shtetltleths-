from readability import Readability

post = """Amir Michail has asked me to comment on his proposal to create a new field: one that’s “like computer science, but more creative.” My first reaction was to wonder, how much more creative does he want? He might as well ask for a field that’s like dentistry, but with more teeth. (I was reminded of Hilbert’s famous remark, when told that a student had abandoned math to become a poet: “Good. He didn’t have enough imagination to be a mathematician.”)

But on second thought, it’s true that computer science encourages a particular kind of creativity: one that’s directed toward answering questions, rather than building things that are useful or cool. I learned about this distinction as an undergraduate, when the professor in my natural language processing class refused to let me write a parody-generating program (like this one) for my term project, on the grounds that such a program would not elucidate any scientific question. Of course, she was right.

Paul Graham explained the issue memorably in his essay Hackers and Painters:

I’ve never liked the term “computer science.” The main reason I don’t like it is that there’s no such thing. Computer science is a grab bag of tenuously related areas thrown together by an accident of history, like Yugoslavia. At one end you have people who are really mathematicians, but call what they’re doing computer science so they can get DARPA grants. In the middle you have people working on something like the natural history of computers — studying the behavior of algorithms for routing data through networks, for example. And then at the other extreme you have the hackers, who are trying to write interesting software, and for whom computers are just a medium of expression, as concrete is for architects or paint for painters …

The mathematicians don’t seem bothered by this. They happily set to work proving theorems like the other mathematicians over in the math department, and probably soon stop noticing that the building they work in says “computer science” on the outside. But for the hackers this label is a problem. If what they’re doing is called science, it makes them feel they ought to be acting scientific. So instead of doing what they really want to do, which is to design beautiful software, hackers in universities and research labs feel they ought to be writing research papers.

(Incidentally, Graham is mistaken about one point: most theoretical computer scientists could not blend in among mathematicians. Avi Wigderson, one of the few who can and does, once explained the difference to me as follows. Mathematicians start from dizzyingly general theorems, then generalize them even further. Theoretical computer scientists start from incredibly concrete problems that no one can solve, then find special cases that still no one can solve.)

One puzzle that Graham’s analysis helps to resolve is why computer systems papers are so excruciatingly boring, almost without exception. It can’t be because the field itself is boring: after all, it’s transformed civilization in 30 years. Rather, computer systems papers are boring because asking hackers to write papers about what they hacked is like asking Bach to write papers about his sonatas:

Abstract. We describe several challenges encountered during the composition of SONATA2 (“Sonata No. 2 in A minor”). These results might provide general insights applicable to the composition of other such sonatas…

So what should be done? Should universities create “Departments of Hacking” to complement their CS departments? I actually think they should (especially if the split led to more tenure-tracks for everyone). All I ask is that, if you do find yourself in a future Hacking Department, you come over to CS for a course on algorithms and complexity. It’ll be good for your soul.
"""
r= Readability(post)
print(r.flesch_kincaid())