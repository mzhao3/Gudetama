# Team Gudetama : Derek Song, Susan Lin, Cheryl Qian, and Simon Tsui (PM)
# SoftDev pd8
# P #00 Da Art of Storytellin'
# 2018-10-23

from flask import Flask, render_template, request, session, redirect, url_for, flash

from os import urandom

import db

app = Flask(__name__)
app.secret_key = urandom(32)
session = {}

#home root
@app.route('/', methods=["POST", "GET"])
def home():
     if 'user' in session:
         titles = db.getEntryTitle(session['user'])
         entries = db.getEntryBody(session['user'])
         dates = db.getEntryDate(session['user'])

         titles=[x[0] for x in titles if x[0] != "CREATED"]
         entries=[x[0] for x in entries if x[0] != "CREATED"]
         dates=[x[0] for x in dates]

         return render_template('return.html', user=session['user'], titles=titles, entries=entries, dates=dates)
     return render_template('form.html')

#reading in user and password, checking to see if it is valid or not
@app.route('/auth', methods=["POST", "GET"])
def login():
    username = request.args['user']
    password = request.args['pass']

    if db.isUser(username) and db.getPw(username) == password and username == "admin":
        session['user'] = 'admin'
        return redirect("/admin")

    #username and passwords match
    if db.isUser(username) and db.getPw(username) == password:
        session['user'] = username
        return redirect('/')

    #username doesn't match
    elif db.isUser(username) == False:
        flash("username not found")
        return render_template('form.html', error=True)

    #password doesn't match username
    elif db.getPw(username) != password:
        flash("password incorrect")
        return render_template('form.html', error=True)

@app.route("/register", methods=['POST', 'GET'])
def register():
    username = request.args["Username"]
    password = request.args['Password']
    blog = request.args['Blog']

    if db.isUser(username):
        flash("user already exists")
        return render_template('form.html', error=True)

    elif db.isUser(username) == False:
        db.register(username, blog, password, "RW")
        flash("Account successfully created")
        return render_template('form.html', success=True)

@app.route("/createBlog", methods=["POST", "GET"])
def createBlog():
    return render_template('createBlog.html')

@app.route("/create", methods=["POST","GET"])
def create():
     title = request.args['entryTitle']
     entry = request.args['entryText']

     db.addEntry(session['user'],title,entry)
     return redirect('/')

@app.route("/edit", methods=["POST", "GET"])
def edit():
    return render_template("edit.html")

@app.route("/search", methods=["POST", "GET"])
def search():
    user = request.args['user']
    if db.isUser(user) == True:
        print("ok")
        titles = db.getEntryTitle(user)
        entries = db.getEntryBody(user)

        titles=[x[0] for x in titles if x[0] != "CREATED"]
        entries=[x[0] for x in entries if x[0] != "CREATED"]

        return render_template("search.html", user=user, titles=titles, entries=entries)
    else: #Error handling
        flash("Username not found! Returned back to your page")
        return redirect("/")

@app.route("/admin", methods = ["POST", "GET"])
def admin():
    users = db.getallUsers()
    blogs = db.getallBlogs()
    dates = db.getallDates()
    return render_template("admin.html", users=users, blogs=blogs, dates=dates)

@app.route("/delete", methods = ["POST", "GET"])
def delete():
    user = request.args['user']
    print(user)
    db.clear(user)
    return redirect(url_for("logout"))

# logout route, sends user back to home root and forgets current user
@app.route("/logout", methods=["POST", "GET"])
def logout():
     session.pop('user')
     return redirect(url_for('home'))

if __name__ == "__main__":
    app.debug = True
    app.run()
