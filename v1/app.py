from flask import Flask, render_template, request, session, redirect, url_for, flash
from os import urandom
import db

app = Flask(__name__)
app.secret_key = urandom(32)
hard_login = {"a": "b"}

@app.route("/")
def start():
    return render_template("home.html")

@app.route("/auth")
def login():
    session["user"] = request.args["username"]
    session["pswd"] = request.args["password"]
    if(session["user"] in hard_login and session['pswd'] == hard_login[session["user"]]):
        return render_template("logged.html", user = session["user"]);
    elif(session["user"] not in hard_login):
        flash ("Username not found")
        return render_template("register.html")
    else:
        flash ("username or password is invalid")
        return render_template("failed.html")

@app.route("/maker")
def createAcct():
    #code for making account here
    db.register(request.args['username'], request.args['blog'], request.args['password'], "Y")
    flash("Account created")
    return render_template("home.html")

# @app.route("/premake")
# def accessRegister():
#     return render_template("register.html")

if __name__ == "__main__":
    app.debug = True
    app.run()
