#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect("scorelib.dat")
cur = conn.cursor()
script = open("scorelib.sql","r")
cur.executescript(script.read())
script.close
conn.commit()
conn.close()