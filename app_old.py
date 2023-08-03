from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from waitress import serve
from flask_restful import Resource, Api

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TimeField, DateField, SelectField, EmailField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, date
import uuid as uuid
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

load_dotenv()
DB_SERVER = os.getenv('DB_SERVER')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_SERVER
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = SECRET_KEY

def getComputerslist():
	retults = Computers.query.order_by(Computers.name)
	returns = [("","")]
	for row in retults:
		returns.append((row.id,row.name))
	return returns

@app.route('/', methods=['GET','POST'])
def home():
    form=SearchForm()
    form.computer.choices = getComputerslist()

    if request.method == 'POST':
        text = form.search.data
        computer = form.computer.data
        # test = Changelog.computer==computer, Changelog.name.like("%poop%")
        # logs = Changelog.query.where(test)
        logs = Changelog.query.where(Changelog.computer==computer, Changelog.date>=form.date_start.data, Changelog.date <= form.date_end.data, Changelog.time >= form.time_start.data, Changelog.time <= form.time_end.data).filter(Changelog.name.like(f"%{text}%"))
        form.search.default=form.search.data
        form.computer.default=form.computer.data
        form.date_start.default = form.date_start.data
        form.time_start.default = form.time_start.data
    else:
         today = date.today()
         starttime = datetime.strptime("06::00::00", '%H::%M::%S').time()
         endtime = datetime.strptime("17::00::00", '%H::%M::%S').time()
         logs = Changelog.query.where(Changelog.date>=today, Changelog.date <= today, Changelog.time >= starttime, Changelog.time <= endtime)
         form.date_start.default = today
         form.date_end.default = today
         form.time_start.default = starttime
         form.time_end.default = endtime

    
    form.process()
    # return "test"
    return render_template("home.html",
                           form=form,
                           logs=logs)



class AddChangeLog(Resource):
     def post(self):
          if request.is_json:
               computer = request.json['computer']
               computer_check = Computers.query.filter_by(name=computer).first()
               if not computer_check:
                    new_computer = Computers(name=computer,code=0)
                    db.session.add(new_computer)
                    db.session.commit()
                    computerid = new_computer.id
               else:
                    computerid = computer_check.id
               log = Changelog(type=request.json['type'], 
                               name=request.json['name'],
                               date=datetime.strptime(request.json['date'], '%m/%d/%Y'),
                               time=request.json['time'],
                               computer=computerid)
               db.session.add(log)
               db.session.commit()
               return make_response(jsonify({'id':log.id}), 201)
          else:
               return {'error': 'request must be json'}, 400

api.add_resource(AddChangeLog, '/api/watch')

class SearchForm(FlaskForm):
    date_start = DateField(validators=[DataRequired()])
    date_end = DateField(validators=[DataRequired()])
    time_start = TimeField(validators=[DataRequired()])
    time_end = TimeField(validators=[DataRequired()])
    search = StringField("Search For?")
    computer = SelectField("Computer Name")
    submit = SubmitField("Search")

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


serve(app, host='0.0.0.0', port=5050, threads=1) #WAITRESS!