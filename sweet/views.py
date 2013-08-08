from flask import Flask, Blueprint, render_template, request, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from model import app, db
import config, json, urllib2
from datetime import datetime, date, timedelta
from policyManager import *
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

@views.route("/check_sensor_repository/<method>")
def check_sensor_repository(method): 

	light = light_data() 
	motion = motion_data() 
	#return render_template("/sensor.html")
	if method == 'light':
		return render_template("/panel_sensor.html", title="light", data=light)
	elif method == 'motion':
		return render_template("/panel_sensor.html", title="motion", data=motion)
	return "@@"
	
@views.route("/sensor_data")
def get_sensor_repository_data():

	light = light_data() 
	motion = motion_data() 
	#return render_template("/sensor.html")
	#return render_template("/panel_sensor.html", data=cleaned_data)
	return jsonify(data={'motion':motion, 'light':light})

def motion_data(): 
	url = 'http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/motion/json'
	data = json.load(urllib2.urlopen(url))
	#problems = []
	cleaned_data = []
	for row in data:
		firefly_time = datetime.fromtimestamp(row['timestamp']/1000).date()
		today_time = datetime.today().date()
		if today_time == firefly_time and row['device_id'] != "test" and row['device_id'] != "test-device" and row['device_id'] != "0":
			if mapping_table.has_key(row['device_id']):
				row['timestamp'] = datetime.fromtimestamp(row['timestamp']/1000)
				row['location'] = mapping_table[row['device_id']][2]
				cleaned_data.append(row)
	#print cleaned_data
	cleanend_data = sorted(cleaned_data, key=lambda tup: tup["device_id"]) 
	return cleaned_data

def light_data(): 
	url = 'http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/light/json'
	data = json.load(urllib2.urlopen(url))
	#problems = []
	cleaned_data = []
	for row in data:
		firefly_time = datetime.fromtimestamp(row['timestamp']/1000).date()
		today_time = datetime.today().date()
		if today_time == firefly_time and row['device_id'] != "test" and row['device_id'] != "test-device" and row['device_id'] != "0":
			if mapping_table.has_key(row['device_id']):
				row['timestamp'] = datetime.fromtimestamp(row['timestamp']/1000)
				row['location'] = mapping_table[row['device_id']][2]
				cleaned_data.append(row)
	#print cleaned_data
	cleanend_data = sorted(cleaned_data, key=lambda tup: tup["device_id"]) 
	return cleaned_data

@views.route("/")
def home():
	return render_template("problem_map.html")

@views.route("/about")
def about():
	return render_template("sweet_building_greeter.html")

@views.route("/transportation")
def transportation():
	return render_template("transportation.html")
