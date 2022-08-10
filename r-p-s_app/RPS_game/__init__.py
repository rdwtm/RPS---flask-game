import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask import Flask
from RPS_game.routes import game_routes

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    load_dotenv()
    from .models import User, Game

    app_env = os.environ.get("FLASK_ENV", "development")
    secret_key = os.environ.get("SECRET_KEY", "dfl;gv,' z l")
    testing = False

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(ENV=app_env, SECRET_KEY=secret_key, TESTING=testing)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(game_routes)

    db.init_app(app)
    create_database(app)

    return app


def create_database(app):
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
