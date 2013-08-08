from flask import Flask, Blueprint, render_template, request, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from model import app, db
import config
from datetime import datetime, date, timedelta
#blueprint
views = Blueprint('views', __name__)

### testing ### 
@views.route("/beauty")
def beauty():
	return render_template("index.html")
@views.route("/nasa")
def nasa_23():
	return render_template("index2.html")
@views.route("/mobile")
def mobile_webpage():
	return render_template("mobile.html")


@views.route("/panel")
def visualize_feedback():
	condition_usage = []
	start_date = datetime.fromordinal(date(2013, 7, 1).toordinal())
	end_date = datetime.fromordinal(date.today().toordinal())
	while start_date != end_date:
		feedbacks = get_list_feedbacks(2013, start_date.month, start_date.day, 9)
		row = {} 
		row['number'] = len(feedbacks);
		row['time'] = start_date.strftime("%Y-%m-%d %H:%M:%S");
		condition_usage.append(row)
		start_date = start_date + timedelta(days=1)
		
	return render_template("panel.html", usage=condition_usage)

@views.route("/")
def home():
	return render_template("problem_map.html")

@views.route("/about")
def about():
	return render_template("sweet_building_greeter.html")

@views.route("/transportation")
def transportation():
	return render_template("transportation.html")
