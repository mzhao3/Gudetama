import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

def getUser(name, word):
    c.execute("CREATE TABLE IF NOT EXISTS usersDirectory(username TEXT, blogName TEXT, password TEXT, permissions TEXT)")
