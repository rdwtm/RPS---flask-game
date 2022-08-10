from . import db
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    cr_points = db.Column(db.Integer)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gamer = db.Column(db.Integer, db.ForeignKey("User.id"))
    result = db.Column(db.String(20))
    nb_cr = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())


def add_rec(note):
    db.session.add(note)
    db.session.commit()


def edit_rec(note):
    db.session.commit()


def max_id(key):
    x = db.session.query(key).all()
    return max(x)
