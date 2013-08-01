from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from sqlalchemy.sql import func
from model import *
import config
from members import *
from datetime import datetime, timedelta
import time
import pytz
import json 
import urllib2
from random import choice

bluetooths = Blueprint('bluetooths', __name__)

@bluetooths.route("/bluetooth_around", methods=['GET'])
def bluetooth_around(): 
	nearby_device = request.args.get("device_id", -1)
	bluetooth_id = request.args.get("bluetooth_id", "")
	device_name = request.args.get("device_name", "")
	#user = get_user_from_bluetooth_id(bluetooth_id)
	bluetooth_around_event = None
	#if user is not None: 
	if bluetooth_id != "" and device_name != "" and nearby_device != -1:
		bluetooth_around_event = DeviceAround(nearby_device, bluetooth_id, device_name)
		db.session.add(bluetooth_around_event)
		db.session.commit()
	else:
		return jsonify(suck=True)
	return jsonify(data=bluetooth_around_event.serialize)