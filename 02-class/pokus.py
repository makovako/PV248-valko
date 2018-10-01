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

text = "Editor: Böhmová, Z., Grünfeldová, A., Sarauer, A."
r = re.compile(r"Editor: (.*)")
m = r.match(text)
# print(m.group(1))

for edit in m.group(1).split(","):
    edit.strip()
    print(edit)
