#!/usr/bin/python3

import sys, sqlite3
import json

conn = sqlite3.connect("scorelib.dat")
cur = conn.cursor()
cur.execute("select person.name,born,died from person join score_author on person.id = score_author.composer join score on score.id = score_author.score join edition on edition.score = score.id join print on print.edition=edition.id where print.id = ?",(int(sys.argv[1]),))
persons = cur.fetchall()

out = []
for person in persons:
    dic = {}
    dic["name"] = person[0]
    if person[1] is not None:
        dic["born"] = person[1]
    if person[2] is not None:
        dic["died"] = person[2]
    out.append(dic)
print(json.dumps(out,indent=4,ensure_ascii=False))

conn.commit()
conn.close()