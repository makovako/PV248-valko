#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect("scorelib.dat")
cur = conn.cursor()
# cur.execute("CREATE TABLE person ( id integer primary key not null, born integer, died integer, name varchar not null);")
cur.execute("INSERT INTO person (id,born,died,name) VALUES (?,?,?,?)",(5,2000,2001,"Bach"))
conn.commit()