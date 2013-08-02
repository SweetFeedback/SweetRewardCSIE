from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import app, db, Problem, Feedback, Member, Window, Location
import config

from datetime import datetime 
import pytz
#blueprint
members = Blueprint('members', __name__)

@members.route("/members")
def list_members():
	members = Member.query.all()
	return jsonify(data=[i.serialize for i in members])
@members.route("/members/user_id")
def get_user(): 
	user = None 
	token = request.args.get("token", "")
	facebook_id = request.args.get("facebook_id", "")
	account = request.args.get("account", "")
	gcm_id = request.args.get("gcm_id", "")
	bluetooth_id = request.args.get("bluetooth_id", "")
	if token is not "": 
		user = get_user_from_token(token)
	elif facebook_id is not "":
		user = get_user_from_fb(facebook_id)
	elif account is not "": 
		user = get_user_from_account(account)
	elif gcm_id is not "":
		user = get_user_from_gcm_id(gcm_id)
	elif bluetooth_id is not "":
		user = get_user_from_bluetooth_id(bluetooth_id)
	return jsonify(user=user.serialize)

def get_user_from_token(token):
	if token is not None and token != "":
		user = db.session.query(Member).filter_by(token=token).first()
		if user is not None:
			return user
	return None
def get_user_from_fb(facebook_id):
	if facebook_id is not None and facebook_id != "":
		user = db.session.query(Member).filter_by(facebook_id=facebook_id).first()
		if user is not None:
			return user
	return None
def get_user_from_account(account):
	if account is not None and account != "":
		user = db.session.query(Member).filter_by(account=account).first()
		if user is not None:
			return user
	return None
def get_user_from_gcm_id(gcm_id):
	if gcm_id is not None and gcm_id != "": 
		user = db.session.query(Member).filter_by(gcm_id=gcm_id).first() 
		if user is not None: 
			return user
	return None
def get_user_from_bluetooth_id(bluetooth_id):
	if bluetooth_id is not None and bluetooth_id != "": 
		user = db.session.query(Member).filter_by(bluetooth_id=bluetooth_id).first() 
		if user is not None: 
			return user
	return None