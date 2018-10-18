# Team Gudemata : Derek Song, Susan Lin, Cheryl Qian, and Simon Tsui (PM)
# SoftDev pd8
# P #00 Da Art of Storytellin'
# 2018-10-23

from flask import Flask, render_template, request, session, redirect, url_for, flash
from os import urandom
import db

app = Flask(__name__)

app.secret_key = urandom(32)
#hard coded valid username and password
users = {"s": "1"}

#home root
@app.route('/', methods=["POST", "GET"])
def home():
     if 'slin15' in session:
          return ('return.html')
     return render_template('form.html')

#reading in user and password, checking to see if it is valid or not
@app.route('/auth', methods=["POST", "GET"])
def login():
    #username and passwords match
    if request.args['user'] in users.keys() and users[request.args['user']] == request.args['pass']:
        return render_template('return.html', user=request.args['user'])

    #username doesn't match
    elif request.args['user'] not in users.keys():
        flash("username not found")
        return render_template('form.html', error=True)

    #password doesn't match username
    elif users[request.args['user']] != request.args['pass']:
        flash("password incorrect")
        return render_template('form.html', error=True)

# logout route, sends user back to home root and forgets current user
@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop['slin15']
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.debug = True
    app.run()
