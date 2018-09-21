#!/usr/bin/python3

import sys
from collections import Counter
import re

composer = Counter()


for line in open(sys.argv[1],"r"):
    if sys.argv[2] == "composer":
        r = re.compile(r"Composer: (.*)")
        m = r.match(line)
        # if line doesnt start with Composer, skip
        if m is None:
            continue
        rawcomp = m.group(1)
        comp = rawcomp.split(";")
        # try every composer after spliting by ";
        for c in comp:
            if not c:
                continue
            c.strip()
            # match and delete () with year
            s = re.compile(r"(.*) \(")
            n = s.match(c)
            if n is not None:
                # if matched, use that version
                composer[n.group(1).strip()] += 1
            else:
                #otherwise use version before matching
                composer[c.strip()] += 1
        
if sys.argv[2] == "composer":
    for c,n in composer.items():
        print(c + ": "+ str(n))
        