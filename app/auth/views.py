from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_required, login_user, logout_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..utils import db


authblp=Blueprint("auth", __name__)

login_manager = LoginManager()

@login_manager.user_loader
def user_loader(id):
    return User.query.get(int(id))


@authblp.route('/home')
def home ():
    return render_template("home.html")

@authblp.route("/signup", methods=["GET", "POST"])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password_hash= request.form.get("password")
    confirm = request.form.get("confirm")

    if request.method == "POST":
        email_exist=User.query.filter_by(email=email).first()
        user_exist=User.query.filter_by(username=username).first()

        password =generate_password_hash(password_hash)
        if password and confirm:
            if email_exist:
                flash("Email already exists, enter a new one.")
            elif user_exist:
                flash("Username already exists, enter a new one")
            else:
                new_user = User(username=username, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()

                return redirect(url_for("login"))
        else:
            return render_template("signup.html")
            
        
    return render_template("signup.html")

@authblp.route("/login", methods=["GET", "POST"])
def login():
    username=request.form.get("username")
    

    if request.method == "POST":
        user= User.query.filter_by(username=username).first()
        password = request.form.get("password")

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/home")
        
        else:
            flash("Username and password does not match")
        
    return render_template("login.html")
        


@authblp.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template("home.html")