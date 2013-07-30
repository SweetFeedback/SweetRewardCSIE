from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from model import app, db
import config

#blueprint
views = Blueprint('views', __name__)

@views.route("/hello")
def hello():
        return "Hello World!"

@views.route("/beauty")
def beauty():
	return render_template("index.html")
@views.route("/nasa")
def nasa_23():
	return render_template("index2.html")
@views.route("/mobile")
def mobile_webpage():
	return render_template("mobile.html")
@views.route("/problem_map")
def problem_map():
	return render_template("problem_map.html")
@views.route("/")
def home():
	return render_template("sweet_building_greeter.html")
@views.route("/questionaire")
def question():
	return render_template("quiz.html")
@views.route("/short_questionnaire")
def short_question():
	return render_template("short_quiz.html")
### worker part ###
@views.route("/test")
def yo(x=16, y=16):
	x = int(request.args.get("x", x))
	y = int(request.args.get("y", y))
	res = add.apply_async((x, y))
	return res.task_id

@views.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=5.0)
    return repr(retval)
