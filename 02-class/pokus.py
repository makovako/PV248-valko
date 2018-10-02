#!/usr/bin/python3

import re
# text = "Composer: Haydn, Joseph; Mozart, Wolfgang Amadeus (1756--1791)"
# r = re.compile(r"Composer: (.*)")
# m = r.match(text)

# for comp in m.group(1).split(';'):
#     s = re.compile(r"(.*) \((.*)\)")
#     n = s.match(comp)
#     print(n.group(1))
#     if n.group(2) is not None:
#         print(n.group(2))

text1 = "Böhmová, Z., Grünfeldová, A., Sarauer, A."
text2 = "Miloslav Klement, Jozef Zsapka"
text3 = "Jean-Claude Veilhan, Guy Robert"
text4 = "Gouin, P."
text5 = "Daniel, Ladislav"
text6 = "David Lasocki, R. P. Block"

# na konci este strip
texts = [text1, text2, text3, text4,text5,text6]

r = re.compile(r"((\w+, \w+.?),?)+")
for text in texts:
    if r.match(text) is not None:
        while text != "":
            m = r.match(text)        
            print(m.group(2))
            text = text.replace(m.group(2), "")[2:]
            print("Left: "+text)
    else:
        comps = text.split(",")
        for comp in comps:
            print(comp)
exit()
m = r.match(text1)
text1 = text1.replace(m.group(2), "")[2:]
print(text1)
m = r.match(text1)
print(m.group(2))
text1 = text1.replace(m.group(2), "")[2:]
print(text1)
m = r.match(text1)
print(m.group(2))
text1 = text1.replace(m.group(2), "")[2:]
print(text1)
exit()
for text in texts:
    m = r.match(text)
    if m is not None:
        # v m.group 2
        print(m.group(2))
    else:
        # split ","
        print(text)
    
