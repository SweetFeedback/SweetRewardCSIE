from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import app, db, Problem, Feedback, Member, Window, Location
import config

from datetime import datetime 
import pytz
#blueprint
reports = Blueprint('reports', __name__)

@reports.route("/reports")
def show_reports():
	problems = Problem.query.all()
	return jsonify(data=[i.serialize for i in problems])

@reports.route("/reports/solved")
def show_reports_solved():
	## give solved problem 
	problems = Problem.query.filter(Problem.status == 1).all()
	return jsonify(data=[i.serialize for i in problems])

@reports.route("/reports/unsolved")
def show_reports_unsolved():
	## give unsolved problem 
	problems = Problem.query.filter(Problem.status == 0).all()
	return jsonify(data=[i.serialize for i in problems])

@reports.route("/reports/locations/<room_id>")
def show_reports_room(room_id):
	## filter by room_id 
	problems = Problem.query.filter(Problem.room_id == room_id).all()
	return jsonify(data=[i.serialize for i in problems])

@reports.route("/reports/insert", methods=['GET', 'POST'])
def insert_report():
	title = request.args.get("title", "")
	content = request.args.get("content", "")
	coor_x = request.args.get("coor_x", 0)
	coor_y = request.args.get("coor_y", 0)
	user_id = request.args.get("user_id", 0)
	category = request.args.get("category", 0)
	room_id = request.args.get("room_id", 0)
	report = Problem(category, room_id, title, content, coor_x, coor_y, user_id)
	db.session.add(report)
	db.session.commit()

	return jsonify(data=[report.serialize], success=1)

@reports.route("/reports/update/<report_id>", methods=['GET', 'POST'])
def update_report(report_id):	
	user_id = request.args.get("user_id", 0)
	target_problem = Problem.query.filter_by(problem_id = report_id).first()
	if target_problem is not None:
		target_problem.status = 1
		target_problem.updated_by = user_id
		db.session.commit()
		return_result = jsonify(data=[target_problem.serialize])
	else:
		return_result = jsonify(error=["can't find this problem from database"])
	return return_result