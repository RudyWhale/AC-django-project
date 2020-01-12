import os, sys, sqlite3
dbfile = "db.sqlite3"
db = sqlite3.connect(dbfile)
cursor = db.cursor()
cursor.execute("select sql from sqlite_master where sql not NULL")
for row in cursor.fetchall():
        print(row[0])
db.close()