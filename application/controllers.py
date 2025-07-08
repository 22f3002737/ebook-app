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
          return redirect("/admin")
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

@app.route("/admin")
def admin():
  users = len(User.query.all())-1
  reqs = len(Ebook.query.filter_by(status="requested").all())
  grants = len(Ebook.query.filter_by(status="granted").all())
  avail = len(Ebook.query.filter_by(status="available").all())
  this_user = User.query.filter_by(type="admin").first()
  req_ebooks = Ebook.query.filter_by(status="requested").all()
  return render_template("admin_dash.html", this_user=this_user,req_ebooks=req_ebooks,users=users,reqs=reqs,grants=grants,avail=avail)

@app.route("/create-ebook", methods=["GET", "POST"])
def create():
  this_user= User.query.filter_by(type="admin").first()
  if request.method == "POST":
    name= request.form.get("name")
    author = request.form.get("author")
    url = request.form.get("url")
    ebook = Ebook(name=name, author=author,url=url)
    db.session.add(ebook)
    db.session.commit()
    return render_template("admin_dash.html",this_user=this_user)
  return render_template("create_eb.html")

@app.route("/request-ebook/<int:user_id>")#button in user dashboard
def request_ebook(user_id):
  this_user = User.query.filter_by(id=user_id).first()
  ebooks = Ebook.query.filter_by(status="available").all()
  return render_template("request.html", this_user=this_user, ebooks=ebooks)

@app.route("/request/<int:ebook_id>/<int:user_id>")#button in request.html
def req_eb(ebook_id,user_id):
  this_user = User.query.get(user_id)
  ebook = Ebook.query.get(ebook_id)
  ebook.status="requested"
  ebook.user_id = user_id
  db.session.commit()
  return render_template("user_dash.html", this_user=this_user)

@app.route("/grant/<int:ebook_id>/<int:user_id>")
def grant_eb(ebook_id,user_id):
  this_user = User.query.get(user_id)
  # ebook = Ebook.query.get(ebook_id)
  ebook= Ebook.query.filter_by(id=ebook_id,user_id=user_id).first()
  ebook.status="granted"
  db.session.commit()
  return redirect("/admin")