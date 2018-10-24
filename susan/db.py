import sqlite3   #enable control of an sqlite database

import csv       #facilitates CSV I/O

from datetime import datetime

DB_FILE="gudetama.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS userDirectory(username TEXT, blogName TEXT, password TEXT, permissions TEXT)")
c.execute("INSERT INTO userDirectory VALUES('admin','admin','admin','all')")
db.commit()
db.close()

def isUser(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT username FROM userDirectory WHERE username = '{0}'".format(user))
    name = c.fetchone()
    db.commit()
    db.close()
    if name != None and len(name) > 0:
        return True
    return False

isUser('admin')

def getPw(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT password FROM userDirectory WHERE username = '{0}'".format(user))
    x = c.fetchone()
    db.commit()
    db.close()
    return x[0]

def resetPw(user, newPass):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("UPDATE userDirectory SET password = newPass WHERE username = '{0}'".format(user))
    db.commit()
    db.close()

def getBlog(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT blogName FROM userDirectory WHERE username = '{0}'".format(user))
    x = c.fetchone()
    db.commit()
    db.close()
    return x

def getBlogTitle(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT title FROM '{0}' WHERE username = '{1}'".format(getBlog(user), user))
    x = c.fetchone()
    db.commit()
    db.close()
    return x

def getBlogBody(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT body FROM '{0}' WHERE username = '{1}'".format(getBlog(user), user))
    x = c.fetchone()
    db.commit()
    db.close()
    return x

def register(user, blog, pw, permission):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS '{0}' (username TEXT, title TEXT, body TEXT, timeB TEXT)".format(blog))
    # creates the user's blog specific database which holds the date of entry, username, title of entry, and content
    c.execute("CREATE TABLE IF NOT EXISTS '{0}' (username TEXT, editedVersion TEXT, title TEXT, timeB TEXT)".format(blog+"History"))
    # creates the user's blog edit history specific database which holds the username, content of edited version, title of entry, and date of edit
    c.execute("INSERT INTO userDirectory VALUES('{0}','{1}', '{2}','{3}')".format(user,blog,pw,permission))
    # inputs username, blog name, password, and permission status into the user Directory database
    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}')".format(blog, user, "CREATED", "CREATED", datetime.utcnow()))
    # first entry of blogName: time is utc standard unless we have time to make user specifc; inserts all information given by user into fields
    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}', '{4}')".format(blog+"History", user, "CREATED", "CREATED", datetime.utcnow()))
    # first entry of blogNameHistory: time is is utc standard unless we have time to make user specifc; inserts all information given by user into fields

    db.commit()
    db.close()

#register('Susan','sblog','pass','read')
##print getPw('Susan')
#print getBlog('Susan')
#resetPw ('Susan', 'word')
#print getPw('Susan')
