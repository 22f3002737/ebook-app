from flask import Flask, render_template, redirect, request
from flask import current_app as app #if you directly import app> circular 
#current _app refers to app object that we created. 
from .models import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

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
        return render_template("incorrect_p.html")
    else:
      return render_template("not_exist.html")
  
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
      return render_template("already.html")
    else:
      user = User(username=username, email=email, password=pwd)
      db.session.add(user)
      db.session.commit()
    return redirect("/login")
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

@app.route("/home/<int:user_id>")
def user_dash(user_id):
    this_user = User.query.filter_by(id=user_id).first()

    return render_template("user_dash.html",this_user=this_user)

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
    return redirect("/admin")
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

@app.route("/view/<ebook>/<int:user_id>")
def view(ebook,user_id):
    this_user = User.query.filter_by(id=user_id).first()
    details = Ebook.query.filter_by(user_id=user_id,name=ebook).all()
    return render_template("view.html",details=details,this_user=this_user)

@app.route("/return/<int:ebook_id>/<int:user_id>")
def return_ebook(ebook_id,user_id):
    return_ebook = Ebook.query.filter_by(id=ebook_id,user_id=user_id).first()
    return_ebook.status="available"
    db.session.commit()
    return redirect(f"/home/{user_id}")

@app.route("/search")
def search():
    search_word = request.args.get("search")
    key = request.args.get("key")
    if key == "user":
        results = User.query.filter_by(username= search_word).all()
    else:
        results = Ebook.query.filter_by(name = search_word).all()
    return render_template("results.html",results=results,key=key)

@app.route("/summary")
def summary():
    av=len(Ebook.query.filter_by(status="available").all())
    re=len(Ebook.query.filter_by(status="requested").all())
    gr=len(Ebook.query.filter_by(status="granted").all())
    #graphs
    #pie chart 
    labels = ["Available","Requested","Granted"]
    sizes =[av,re,gr]
    colors = ["blue","yellow","green"]
    plt.pie(sizes,labels=labels,colors=colors,autopct = "%1.1f%%")
    plt.title("Status of E-books")
    plt.savefig("static/pie.png")
    plt.clf()

    #bar graph 
    labels = ["Available","Requested","Granted"]
    sizes =[av,re,gr]
    plt.bar(labels,sizes)
    plt.xlabel("Status of E-books")
    plt.ylabel("No of E-books")
    plt.title("Ebooks Status Distribution")
    plt.savefig("static/bar.png")
    plt.clf()

    return render_template("summary.html",av=av,re=re,gr=gr)