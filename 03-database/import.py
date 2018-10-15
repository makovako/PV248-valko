#!/usr/bin/python3

from scorelib import Composition,Edition,Person,Print,Voice,load
# edition year nechat null
import sys, sqlite3


# database name
database = sys.argv[2]

def insert_print(pr, cur):
    # check composers
    composer_ids = []
    for comp in pr.edition.composition.authors:
        cur.execute("select id from person where name = {};".format(comp.name))
        composers = cur.fetchall()
        if len(composers) == 1:
            composer_ids.append(composers[0][0])
            # TODO update years if necessary
            # UPDATE Customers SET ContactName = 'Alfred Schmidt', City= 'Frankfurt' WHERE CustomerID = 1;
        else:
            pass
            # TODO create new person and append new id
    # check composition
    # TODO create connection in score authors
    # check eidtors
    # check edition
    # TODO create connection in edition authors
    # check voices
    # TODO need composition id
    # check print

# reset file
f = open(database,"w")
f.close()

conn = sqlite3.connect(database)
cur = conn.cursor()
# create tables from sql script
script = open("scorelib.sql","r")
cur.executescript(script.read())
script.close

prints = load(sys.argv[1])

# for pr in prints:
#     insert_print(pr,cur)

conn.commit()
conn.close()