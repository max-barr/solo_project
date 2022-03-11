from crypt import methods
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_app.models.hike import Hike

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ====ROUTES=====

# Login/register GET request
@app.route("/")
def index():
    return render_template("index.html")

# Register new user POST request
@app.route("/register", methods=["POST"])
def register():
    if not User.validate_registration(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    print(pw_hash)
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect("/dashboard")

# Login POST request
@app.route("/login", methods=["POST"])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid email/password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        flash("Invalid email/password")
        return redirect("/")
    session["user_id"] = user_in_db.id
    return redirect("/dashboard")

#Logout GET request
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# User homepage GET request
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : session["user_id"]
    }
    user = User.get_user_with_hikes(data)
    all_hikes = Hike.get_all()
    return render_template("dashboard.html", user = user, hikes = all_hikes)

# User's created hikes GET request
@app.route("/myhikes")
def display_hikes():
    if "user_id" not in session:
        return redirect("logout")
    data = {
        "id" : session["user_id"]
    }
    user = User.get_user_with_hikes(data)
    print(user)
    return render_template("user_hikes.html", user = user)