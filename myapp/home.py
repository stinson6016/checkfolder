from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, date
from flask_restful import Resource

from .webforms import SearchForm
from .extras import getComputerslist, TYPES
from .models import Changelog

home = Blueprint("home", __name__)


@home.route('/')
def homepage():
    form=SearchForm()

    today = date.today()
    starttime = datetime.strptime("06::00::00", '%H::%M::%S').time()
    endtime = datetime.strptime("17::00::00", '%H::%M::%S').time()
    logs = Changelog.query.where(Changelog.date>=today, Changelog.date <= today, Changelog.time >= starttime, Changelog.time <= endtime)
    form.date_start.default = today
    form.date_end.default = today
    form.time_start.default = starttime
    form.time_end.default = endtime
    
    form.computer.choices = getComputerslist()
    form.process()
    return render_template("home.html",
                           form=form,
                           logs=logs,
                           types=TYPES)

@home.route('/search', methods=['GET','POST'])
def search():
    if request.method != "POST":
        return redirect(url_for('home.homepage'))
    form = SearchForm()
    text = form.search.data
    computer = form.computer.data
    logs = Changelog.query.where(Changelog.computer==computer, Changelog.date>=form.date_start.data, Changelog.date <= form.date_end.data, Changelog.time >= form.time_start.data, Changelog.time <= form.time_end.data).filter(Changelog.name.like(f"%{text}%"))
    form.search.default=form.search.data
    form.computer.default=form.computer.data
    form.date_start.default = form.date_start.data
    form.time_start.default = form.time_start.data
    form.computer.choices = getComputerslist()
    form.process()
    return render_template("home.html",
                        form=form,
                        logs=logs,
                        types=TYPES)