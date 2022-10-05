from flask import Flask, render_template, redirect, url_for, session, g, flash, Markup, request, make_response
from forms import RegistrationForm, LoginForm, RoomForm, ScheduleForm
from database import get_db, close_db
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from random import sample
from itertools import * 

# BEST VIEWED ON PC/LAPTOP

# adding comment to test

app = Flask(__name__)
app.config["SECRET_KEY"] = "we-are-the-best"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

''' Testing purposes login
    username: test-dev
    password zxc10!Z
'''

@app.teardown_appcontext
def close_db_at_end_of_requests(e=None):
    close_db(e)

@app.before_request
def logged_in():
    g.user = session.get("username", None)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login"))
        return view(**kwargs)
    return wrapped_view

# 404 error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('oh_no.html', name="Error"), 404

# Home page
@app.route("/")
def index():
    db = get_db() 
    return render_template("index.html", name="Home")

# About page
@app.route("/about")
def about():
    return render_template("about.html", name="About")

# Our Solution page
@app.route("/product")
def product():
    db = get_db()
    return render_template("product.html", name="Our Solution")

# Product Demo page
@app.route("/demo")
def demo():
    return render_template("demo.html", name="Demo")

# Register for an account
@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data

        db = get_db()
        if db.execute("""SELECT * FROM users WHERE email =?;""", (email,)).fetchone() is not None:
            form.email.errors.append("Sorry, the email you entered already exists, please use another email.")
        elif db.execute("""SELECT * FROM users WHERE username =?;""", (username,)).fetchone() is not None:
            form.username.errors.append("Sorry, the username you entered already exists, please create a new username.")
        elif password.isupper() or password.isdigit() or password.islower() or password.isalpha():
            form.password.errors.append("Create a STRONG password with one uppercase character, one lowercase character and one number")
        else:
            db.execute("""INSERT INTO users (username, email, password)
                        VALUES (?,?,?);""", (username, email, generate_password_hash(password)))
            db.commit()
            flash("Successful Registration! Please login now")
            return redirect( url_for("login"))
    return render_template("register.html", form=form, name="Register")

# Shows terms and conditions
@app.route("/terms")
def terms():
    return render_template("terms_con.html", name="Terms and Conditions")

# Login to account
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data
        
        db = get_db() 
        user = db.execute("""SELECT * FROM users WHERE username = ?;""", (username,)).fetchone()

        if 'counter' not in session:
            session['counter'] = 0

        if user is None:
            form.username.errors.append("Username doesn't exist, please check your spelling")
        elif not check_password_hash(user["password"], password):
            form.password.errors.append("Incorrect password")
            session['counter'] = session.get('counter') + 1
            if session.get('counter')==3:
                flash(Markup('Oh no, are you having trouble logging in? Bruh that sucks'))
                session.pop('counter', None)
        else:
            session.clear()
            session["username"] = username
            return redirect(url_for("profile"))
    return render_template("login.html", form=form, name="Login")

# Logout from account
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Settings page
@app.route("/settings")
def settings():
    return render_template("settings.html", name="Settings")

# Profile page
@app.route("/profile")
def profile():
    return render_template("profile.html", name="My Profile")

# House page
@app.route("/user_house", methods=["GET", "POST"])
def user_house():
    form = RoomForm()
    rooms = None
    if form.validate_on_submit():
        automation = form.automation.data
        name = form.name.data
        
        db = get_db()
        db.execute("""INSERT INTO rooms (username, name, automation)
                        VALUES (?,?,?);""", (g.user, name, automation))
        db.commit()
        
        room = db.execute("""SELECT * FROM rooms WHERE room_id in 
                                (SELECT max(room_id) FROM rooms WHERE username=?);""", (g.user,)).fetchone()
        flash ("Yay! You just created a room! Go ahead and add scheduling times now!") 
        #return redirect(url_for("showRoom", id=room["room_id"]))
        return redirect(url_for("user_house"))
    else:
        db = get_db()
        rooms = db.execute("""SELECT * FROM rooms WHERE username=?;""", (g.user,)).fetchall()
    return render_template("user_house.html", form=form, name="Home", rooms=rooms)

# Room page
@app.route("/show_room/<int:id>")
@login_required
def show_room(id):
    db = get_db()
    room = db.execute("""SELECT * FROM rooms WHERE username=? AND room_id=?;""", (g.user,id)).fetchone()
    return render_template("show_room.html", name="Room", room=room)

# Deletes Room
@app.route("/delete_room/<int:id>")
@login_required
def delete_room(id):
    db = get_db()
    db.execute("""DELETE FROM rooms WHERE username =? AND room_id=?;""", (g.user,id)).fetchone()
    db.commit()
    flash ("Room deleted!")
    return redirect(url_for("user_house"))

#@app.route("/newRoom", methods=["GET", "POST"])

if __name__ == '__main__':
    app.run(debug = True)