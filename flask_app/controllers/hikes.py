from crypt import methods
from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.hike import Hike
from flask_app.models.user import User

# ====ROUTES=====

# Create a new hike GET request
@app.route("/newhike")
def new_hike():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : session["user_id"]
    }
    return render_template("new_hike.html", user = User.get_by_id(data))

# Create a new hike POST request
@app.route("/create/hike", methods=["POST"])
def create_hike():
    if "user_id" not in session:
        return redirect("/logout")
    if not Hike.validate_hike(request.form):
        return redirect("/newhike")
    data = {
        "id" : id,
        "title": request.form["title"],
        "description": request.form["description"],
        "location": request.form["location"],
        "date": request.form["date"],
        "user_id": session["user_id"]
    }
    Hike.save(data)
    return redirect("/dashboard")

# Edit a hike GET request
@app.route("/edit/hike/<int:id>")
def edit_hike(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id" : id
    }
    user_data = {
        "id" : session["user_id"]
    }
    hike = Hike.get_one(data)
    return render_template("edit_hike.html", user = User.get_by_id(user_data), hike = hike)

# Update a hike POST request
@app.route("/update/hike/<int:id>", methods=["POST"])
def update_hike(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id,
        "title" : request.form["title"],
        "description" : request.form["description"],
        "location" : request.form["location"],
        "date" : request.form["date"]
    }
    if not Hike.validate_hike(request.form):
        return redirect("/edit/hike/<int:id>")
    Hike.update(data)
    return redirect("/myhikes")

# Display one hike GET request
@app.route("/hike/<int:id>")
def view_hike(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    hike = Hike.get_one(data)
    print(hike)
    return render_template("view_hike.html", hike = hike)

# Delete a hike GET request
@app.route("/delete/hike/<int:id>")
def destroy_hike(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id" : id
    }
    Hike.destroy(data)
    return redirect("/myhikes")
