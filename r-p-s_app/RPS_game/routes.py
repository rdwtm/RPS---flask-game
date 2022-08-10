from datetime import datetime, timedelta
from flask import Blueprint, request, render_template, session, flash
from game_utils.rock_paper_scissors import *
from sqlalchemy.sql.expression import func

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/")
def index():
    print("VISITING THE START PAGE")
    return render_template("start.html")


@game_routes.route("/choose", methods=["GET", "POST"])
def New_Session(choice=None):

    from .models import User, add_rec, max_id

    new_user = User(cr_points=10)
    print(new_user)
    add_rec(new_user)
    user = User.query.get(max_id(User.id))
    result = {
        "have_credits": True,
        "user_choice": "",
        "computer_choice": "",
        "results_message": "",
        "cr_points": "",
        "user_id": "",
    }

    return render_template("choose.html", credits=user.cr_points, user=user.id)


@game_routes.route("/game", methods=["GET", "POST"])
def game(choice=None):
    from .models import User, Game, add_rec, max_id

    options = ["rock", "paper", "scissors"]
    # CAPTURE INPUTS
    game_stat = Game()
    user = User.query.get(max_id(User.id))
    if user.cr_points > 2:
        have_credits = True
        game_stat.nb_cr = user.cr_points
        user.cr_points -= 3

        add_rec(user)
        if "choice" in request.args:
            user_choice = request.args["choice"]
        elif "choice" in request.values:
            user_choice = request.values["choice"]
        else:
            user_choice = "rock"

        if user_choice not in options:
            user_choice = "rock"

        # PROCESS INPUTS
        computer_choice = random_choice(options)
        winning_choice = determine_winner(user_choice, computer_choice)

        if winning_choice:
            if winning_choice == user_choice:
                results_message = "WYGRANA!!"
                user.cr_points += 4
                add_rec(user)
            elif winning_choice == computer_choice:
                results_message = "Porażka..."
        else:
            results_message = "REMIS"
            user.cr_points += 3

        game_stat.gamer = user.id
        game_stat.result = results_message
        add_rec(game_stat)

        if user_choice == "rock":
            user_choice = "kamień"
        elif user_choice == "paper":
            user_choice = "papier"
        elif user_choice == "scissors":
            user_choice = "nożyce"
        if computer_choice == "rock":
            computer_choice = "kamień"
        elif computer_choice == "paper":
            computer_choice = "papier"
        elif computer_choice == "scissors":
            computer_choice = "nożyce"

        result = {
            "have_credits": have_credits,
            "user_choice": user_choice,
            "computer_choice": computer_choice,
            "results_message": results_message,
            "cr_points": user.cr_points,
            "user_id": user.id,
        }

    else:
        flash(
            "Za mało kredytów. Po wciśnięciu przycisku Dodaj punkty do dyspozycji otrzymasz 10 kredytów",
            category="success",
        )
        result = {
            "have_credits": False,
            "user_choice": "",
            "computer_choice": "",
            "results_message": "",
            "cr_points": user.cr_points,
            "user_id": user.id,
        }
    return render_template(
        "game.html",
        have_credits=result["have_credits"],
        user_choice=result["user_choice"],
        computer_choice=result["computer_choice"],
        results_message=result["results_message"],
        credits=result["cr_points"],
        user=result["user_id"],
        result=result,
    )


@game_routes.route("/add_cr", methods=["GET", "POST"])
def add_cr():
    from .models import User, edit_rec, max_id

    user = User.query.get(max_id(User.id))
    user.cr_points = 10
    edit_rec(user)
    return render_template(
        "game.html", have_credits=True, credits=user.cr_points, user=user.id
    )


@game_routes.route("/game_data", methods=["GET", "POST"])
def game_data():
    from .models import Game

    if request.method == "POST":
        filter_date = request.form.get("date")
        return render_template(
            "game_data.html",
            query=Game.query.filter(func.date(Game.date) == filter_date).all(),
        )
    return render_template("game_data.html", query=Game.query.all())
