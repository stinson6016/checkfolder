from flask import Blueprint, render_template, request, jsonify, make_response
from datetime import datetime, date
from flask_restful import Resource

from .webforms import SearchForm
from .extras import getComputerslist
from .models import Changelog, Computers

home = Blueprint("home", __name__)


@home.route('/', methods=['GET','POST'])
def homepage():
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