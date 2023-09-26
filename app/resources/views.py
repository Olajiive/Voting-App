from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required
from ..models.poll import Poll
from ..models.user import User
from ..utils import db

voteblp=Blueprint("vote", __name__)


@voteblp.route("/")
def home():
    polls = Poll.query.all()
    context = {
        "polls":polls
    }
    return render_template("home.html", **context)

@voteblp.route("/polls/user/<username>")
def userpoll(username):
    
    polls = Poll.query.filter_by(user_id=current_user.id).all()
    username = current_user.username
    context = {
        "polls": polls,
        "username":username
    }
    return render_template("userpoll.html", **context)

@voteblp.route("/create", methods=["GET", "POST"])
def create():
    question= request.form.get("question")
    option_one = request.form.get("option_one")
    option_two = request.form.get("option_two")
    option_three = request.form.get("option_three")

    if request.method == "POST":
        existing_question = Poll.query.filter_by(question=question).first()


        if existing_question:
            flash("Question already exists, kindly input another quesion.")

        else:
            new_poll = Poll(user_id=current_user.id, question= question, option_one=option_one, 
                            option_two=option_two, option_three=option_three)
            
            db.session.add(new_poll)
            db.session.commit()
            return redirect(url_for("vote.userpoll", username=current_user.username))
        
            
    return render_template("create.html")

@voteblp.route("/result/<id>")
def result(id):
    poll = Poll.query.get(id)
    context = {
        "poll": poll
    }
    return render_template ("result.html", **context)


@voteblp.route("/vote/<vote_id>", methods=["GET", "POST"])
def vote(vote_id):
    poll = Poll.query.get_or_404(vote_id)
   
    context = {
        "poll":poll
    }
     
    if request.method == "POST":
        selected_option = request.form.get("option")
        if selected_option == poll.option_one:
            poll.option_one_count += 1
        elif selected_option == poll.option_two:
            poll.option_two_count += 1
        elif selected_option == poll.option_three:
            poll.option_three_count += 1
        else:
            flash("you did'nt select any option")

        db.session.commit()
        return redirect(url_for("vote.result", id=poll.id))

    return render_template("poll.html", **context)

