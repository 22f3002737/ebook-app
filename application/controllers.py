from flask import Flask, render_template, redirect, request
from flask import current_app as app #if you directly import app> circular 
#current _app refers to app object that we created. 
from .models import *

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    pwd = request.form.get("pwd")
    this_user = User.query.filter_by(username=username).first()#lhs>table attribute, rhs>form data
    if this_user:
      if this_user.password == pwd:
        if this_user.type == "admin":
          return render_template("admin_dash.html", this_user=this_user)
        else:
          return render_template("user_dash.html", this_user=this_user)
      else:
        return "password is wrong"
    else:
      return "user does not exist"
  
  return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form["username"]
    email = request.form["email"]
    pwd = request.form["pwd"]
    user_name = User.query.filter_by(username=username).first()
    user_email = User.query.filter_by(email=email).first()
    if user_name or user_email:
      return "user already exists"
    else:
      user = User(username=username, email=email, password=pwd)
      db.session.add(user)
      db.session.commit()
    return "registered successfully"
  return render_template("register.html")