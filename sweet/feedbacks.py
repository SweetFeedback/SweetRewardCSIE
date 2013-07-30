from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import *
import config
from members import *
from datetime import datetime, timedelta, date
import time
import pytz
import json 
import urllib2
from random import choice

#blueprint
feedbacks = Blueprint('feedbacks', __name__)

### method related to feedback 
@feedbacks.route("/feedbacks/<years>/<months>/<days>")
def get_feedbacks(years, months, days):
	print years, months, days 
	date_get = date(int(years), int(months), int(days))
	datetime_converted = datetime.fromordinal(date_get.toordinal())
	date_get_plus_1 = date(int(years), int(months), int(days)+1)
	datetime_converted_end = datetime.fromordinal(date_get_plus_1.toordinal())

	feedbacks = Feedback.query.filter(Feedback.created_time < datetime_converted_end).filter(Feedback.created_time > datetime_converted).all()
	return jsonify(data=[i.serialize for i in feedbacks])

@feedbacks.route("/feedback_insert", methods=['GET'])
def feedback_insert():
	device_id = request.args.get("device_id", -1)
	application_id = request.args.get("application_id", -1)
	user_id = request.args.get("user_id", -1)
	feedback_type = request.args.get("feedback_type", -1)
	feedback_description = request.args.get("feedback_description", "")	
	can_get_time = request.args.get("can_get_time", 0)

	time = None 
	if device_id == -1:
		device_id = get_device_id_from_ip(request.remote_addr)

	if can_get_time != 0:
		time = datetime.now() + timedelta(seconds=int(can_get_time))
	return jsonify(data=insert_feedback(device_id, application_id, user_id, feedback_type, feedback_description, time).serialize)
	
def insert_feedback(device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time=None):
	feedback = Feedback(device_id, app_id, user_id, feedback_type, feedback_desc, can_get_time)
	db.session.add(feedback)
	db.session.commit()
	return feedback

@feedbacks.route("/get_feedback", methods=['GET'])
def feedback():
	device_id = request.args.get("device_id", -1)
	feedbacks = Feedback.query.filter_by(device_id=device_id).filter_by(if_get=False).filter(Feedback.can_get_time <= datetime.now()).all()
	return jsonify(data=[i.serialize for i in feedbacks])

@feedbacks.route("/retrieve_feedback", methods=['GET'])
def retrieve_feedback():
	device_id = request.args.get("device_id", -1)
	feedback_id = request.args.get("feedback_id", -1)
	user_id = request.args.get("user_id", -1)
	feedback = Feedback.query.filter_by(feedback_id=feedback_id).first()
	if feedback is not None: 
		feedback.device_id = device_id
		db.session.commit()
	return jsonify(data=[feedback.serialize])
@feedbacks.route("/get_feedback_by_user", methods=['GET'])
def get_feedback_by_user():
	token = request.args.get("token", -1)
	user = get_user_from_token(token)
	feedbacks = Feedback.query.filter_by(user_id=user.user_id).filter_by(if_get=False).filter(Feedback.can_get_time < datetime.now())
	return jsonify(data=[i.serialize for i in feedbacks])
@feedbacks.route("/update_feedback", methods=['GET'])
def update_feedback():
	feedback_id = request.args.get("feedback_id", -1)
	feedback = db.session.query(Feedback).filter_by(feedback_id=feedback_id).first()
	if feedback is not None:
		feedback.if_get = True
		feedback.retrieve_time = datetime.now()
		db.session.commit()
	return jsonify(data=[feedback.serialize])