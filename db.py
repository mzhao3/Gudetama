import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

DB_FILE="discobandit.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()

c.execute("CREATE TABLE userDirectory(username TEXT, blogName TEXT, password TEXT, permissions TEXT)")
    
def getPw(user):
    c.execute("SELECT password FROM userDirectory WHERE username = '{0}'".format(user))
    return c.fetchone()

def getBlog(user):
    c.execute("SELECT blogName FROM userDirectory WHERE username = '{0}'".format(user))
    return c.fetchone()

def register(user, blog, pw, permission):
    c.execute("INSERT INTO userDirectory VALUES('{0}','{1}', '{2}','{3}')".format(user,blog,pw,permission))


register('Susan','sblog','pass','read')
print getPw('Susan')
print getBlog('Susan')


        


