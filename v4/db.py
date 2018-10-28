import sqlite3   #enable control of an sqlite database

import csv       #facilitates CSV I/O

from datetime import datetime

DB_FILE="gudetama.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()
c.execute("CREATE TABLE IF NOT EXISTS userDirectory(username TEXT, blogName TEXT, password TEXT, permissions TEXT)")
c.execute("INSERT INTO userDirectory VALUES('admin','admin','admin','A')")
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

def getBlogName(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT blogName FROM userDirectory WHERE username = '{0}'".format(user))
    x = c.fetchone()
    db.commit()
    db.close()
    return x[0]

def getEntryTitle(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT title FROM '{0}'".format(user))
    x = c.fetchall()
    db.commit()
    db.close()
    return x

def getEntryBody(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT body FROM '{0}'".format(user))
    x = c.fetchall()
    db.commit()
    db.close()
    return x

def getEntryDate(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT timeB FROM '{0}'".format(user))
    x = c.fetchall()
    db.commit()
    db.close()
    return x

def updateEntry(user, Title, entry):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("UPDATE '{0}' SET body = entry WHERE username = '{1}', title = Title".format(user, user))
    c.execute("INSERT INTO '{0}' (title, editedVersion, timeB) VALUES ('{1}', '{2}', '{3}')".format(user+'History', Title, entry, datetime.utcnow()))
    db.commit()
    db.close()

def addEntry(user, Title, entry):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}')".format(user, Title, entry, datetime.utcnow()))
    db.commit()
    db.close()

def register(user, blog, pw, permission):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS '{0}' (title TEXT, body TEXT, timeB TEXT)".format(user))
    # creates the user's blog specific database which holds the date of entry, username, title of entry, and content

    c.execute("CREATE TABLE IF NOT EXISTS '{0}' (title TEXT, editedVersion TEXT, timeB TEXT)".format(user+"History"))
    # creates the user's blog edit history specific database which holds the username, content of edited version, title of entry, and date of edit

    c.execute("INSERT INTO userDirectory VALUES('{0}','{1}', '{2}','{3}')".format(user,blog,pw,permission))
    # inputs username, blog name, password, and permission status into the user Directory database

    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}')".format(user, "CREATED", "CREATED", datetime.utcnow()))
    # first entry of blogName: time is utc standard unless we have time to make user specifc; inserts all information given by user into fields

    c.execute("INSERT INTO '{0}' VALUES ('{1}', '{2}', '{3}')".format(user+"History", "CREATED", "CREATED", datetime.utcnow()))
    # first entry of blogNameHistory: time is is utc standard unless we have time to make user specifc; inserts all information given by user into fields

    db.commit()
    db.close()

def getallUsers():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT username FROM userDirectory WHERE username != 'admin'")
    x = c.fetchall()
    cat2 = {}
    cat = []
    for i in x:
        cat.append(i[0])
        cat2[i[0]] = getBlogName(i[0]), getBlogName(i[0])+"History"
    db.commit()
    db.close()
    return cat

def getallBlogs():
    dir = getallUsers()
    retList = []
    for i in dir:
        retList.append(getBlogName(i))
    return retList

def getallDates():
    dir = getallUsers()
    retList = []
    for i in dir:
        retList.append(getEntryDate(i)[len(getEntryDate(i))-1][0])
    return retList

def clear(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("DELETE FROM userDirectory WHERE username = '{0}'".format(user))
    if(user != "admin"):
        c.execute("DELETE FROM {0}".format(user, user))
        c.execute("DELETE FROM {0}".format(user+"History", user))
    db.commit()
    db.close()


# def testing():
#     db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
#     c = db.cursor()
#     register("simon", "hi", "h", "RW")
#     c.execute("SELECT * FROM userDirectory")
#     for i in c:
#         print(i)
#     print("BlogNames:", getBlogName("simon"))
#     print("Entry Titles: ", getEntryTitle("simon"))
#     print("All users: ", getallUsers())
#     print("All blogs: ", getallBlogs())
#     print("All dates: ", getallDates())
#     # print()
#     # print()
#     clear("simon")
#     clear("admin")
#
# testing()
