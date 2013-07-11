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
members = Blueprint('members', __name__)

@members.route("/members")
def list_members():
	members = Member.query.all()
	return jsonify(data=[i.serialize for i in members])
@members.route("/members/user_id")
def get_user(): 
	token = request.args.get("token", "")
	facebook_id = request.args.get("facebook_id", "")
	account = request.args.get("account", "")
	gcm_id = request.args.get("gcm_id", "")
	if token is not "": 
		user_id = get_id_from_token(token)
	elif facebook_id is not "":
		user_id = get_id_from_fb(facebook_id)
	elif account is not "": 
		user_id = get_id_from_account(account)
	elif gcm_id is not "":
		user_id = get_id_from_gcm_id(gcm_id)
	return jsonify(user_id=user_id)

def get_id_from_token(token):
	if token is not None:
		user = db.session.query(Member).filter_by(token=token).first()
		if user is not None:
			return user.user_id
	return 0
def get_id_from_fb(facebook_id):
	if facebook_id is not None:
		user = db.session.query(Member).filter_by(facebook_id=facebook_id).first()
		if user is not None:
			return user.user_id
	return 0
def get_id_from_account(account):
	if account is not None:
		user = db.session.query(Member).filter_by(account=account).first()
		if user is not None:
			return user.user_id
	return 0
def get_id_from_gcm_id(gcm_id):
	if gcm_id is not None: 
		user = db.session.query(Member).filter_by(gcm_id=gcm_id).first() 
		if user is not None: 
			return user.user_id
	return 0 