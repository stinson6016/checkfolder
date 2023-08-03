
from . import db


class Changelog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    name = db.Column(db.String(360))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    computer = db.Column(db.Integer)

class Computers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    code = db.Column(db.String(20))

class Types(db.Model):
    code = db.Column(db.Integer, primary_key=True)
    acting = db.Column(db.String(10))
