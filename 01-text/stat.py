#!/usr/bin/python3

import sys
from collections import Counter
import re

composer = Counter()


for line in open(sys.argv[1],"r"):
    # print(line)
    
    if sys.argv[2] == "composer":
        # rozdelit na bodkociarkach, zrusit roky
        r = re.compile(r"Composer: (.*)")
        m = r.match(line)
        if m is None:
            continue
        # print(m.group(1))
        rawcomp = m.group(1)
        comp = rawcomp.split(";")
        for c in comp:
            if not c:
                continue
            c.strip()
            s = re.compile(r"(.*) \(")
            n = s.match(c)
            if n is not None:
                composer[n.group(1).strip()] += 1
            else:
                composer[c.strip()] += 1
        # print(comp)
        # composer[comp] +=1

# print(composer)
if sys.argv[2] == "composer":
    for c,n in composer.items():
        print(c + ": "+ str(n))
        

# print("Hello world")