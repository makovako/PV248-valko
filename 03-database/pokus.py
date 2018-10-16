#!/usr/bin/python3

import sqlite3

conn = sqlite3.connect("test.dat")
cur = conn.cursor()
# script = open("scorelib.sql","r")
# cur.executescript(script.read())
# script.close
cur.execute("drop table person;")
cur.execute("create table person ( id integer primary key not null, name varchar not null );")
cur.execute("insert into person (name) values (?)",("adam",))
# print(cur.fetchall())
cur.execute("insert into person (name) values (?)",("boris",))
# print(cur.rowcount)
cur.execute("insert into person (name) values (?)",("adam",))
# print(cur.rowcount)
cur.execute("select id from person where name = 'adam'")
# print(cur.fetchall())
for i in cur.fetchall():
    print(i[0])
cur.execute("update person set name = ? where id = ?",("jozef",1))
conn.commit()
conn.close()