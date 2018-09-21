#!/usr/bin/python3

import sys
from collections import Counter
import re

# containers holding composer names/ceturies and their count
composer = Counter()
century = Counter()


def year_to_century(year):
    return str((int(year) - 1) // 100 + 1)

# havent found better way, source stack overflow
def is_number(n):
    try:
        int(n)
        return True
    except ValueError:
        return False


for line in open(sys.argv[1],"r"):
    if sys.argv[2] == "century":
        # options: year, year and town, town and year, also with comma,
        # date, range with --, ...th century , ca | ca. year
        r = re.compile(r"Composition Year: (.*)")
        m = r.match(line)
        # if its not line with composition year, skip
        if m is None:
            continue
        cent = m.group(1).strip()
        # if the string is empty
        if not cent:
            continue
        if "century" in cent:
            # if there is word century, split by "t", e. g. 17 | th century
            century[cent.split("t")[0]] += 1
        elif "--" in cent:
            # if its range, take rigth year of the two
            century[year_to_century(cent.rsplit("-",1)[1])] += 1
        elif "ca" in cent:
            # strip city name away
            parsed = cent.split(",")[0].strip()
            # split by " " and year is on the rirght side
            century[year_to_century(parsed.rsplit(" ",1)[1])] += 1
        elif "." in cent:
            # if its a date, split by ".", take year
            century[year_to_century(cent.rsplit(".",1)[1].strip())] += 1
        elif "," in cent:
            # the year and town are seperated by comma
            century[year_to_century(cent.split(",")[0].strip())] += 1
        elif is_number(cent):
            # if we already got only year
            century[year_to_century(cent)] += 1
        else:
            # there are year and town in any order
            parsed = cent.split(" ")
            for p in parsed:
                if is_number(p):
                    century[year_to_century(p)] += 1
        

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
    if False: # change to true to print sorted by number of compositions
        sorted_by_value = sorted(composer.items(), key=lambda kv: kv[1],reverse=True) # source stack overflow
        for c,n in sorted_by_value:
            print(c + ": " + str(n))
    else:
        for c,n in composer.items():
            print(c + ": "+ str(n))

if sys.argv[2] == "century":
    keys = list(century.keys())
    keys.sort()
    for c in keys:    
        print(c + ": " + str(century[c]))