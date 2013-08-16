from flask import Flask, Blueprint, render_template, request, jsonify, json
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from model import app, db
import config, json, urllib2
from datetime import datetime, date, timedelta
from policyManager import *
from api import *
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
	#return render_template("/sensor.html")
	if method == 'light':
		light = light_data() 
		return render_template("/panel_sensor.html", title="light", data=light)
	elif method == 'motion':
		motion = motion_data() 
		return render_template("/panel_sensor.html", title="motion", data=motion)
	elif method == 'digital_temp':
		digital_temp = digital_temp_data()
		return render_template("/panel_sensor.html", title="digital_temp", data=digital_temp)
	elif method == 'temp':
		temp = temp_data()
		return render_template("/panel_sensor.html", title="temp", data=temp)
	elif method == 'humidity':
		humidity = humidity_data()
		return render_template("/panel_sensor.html", title="humidity", data=humidity)
	elif method == 'pressure':
		pressure = pressure_data()
		return render_template("/panel_sensor.html", title="pressure", data=pressure)

	return "@@"
	
@views.route("/sensor_data")
def get_sensor_repository_data():

	light = light_data() 
	motion = motion_data() 
	#return render_template("/sensor.html")
	#return render_template("/panel_sensor.html", data=cleaned_data)
	return '''
	
{
  "data": {
    "light": [
      {
        "device_id": "10170008",
        "location": "B23.212",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:23 GMT",
        "value": 923
      },
      {
        "device_id": "10170302",
        "location": "B23.105B",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:47 GMT",
        "value": 1023
      },
      {
        "device_id": "10170308",
        "location": "B23.120",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:07 GMT",
        "value": 961
      },
      {
        "device_id": "10170104",
        "location": "B23.230",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:49 GMT",
        "value": 944
      },
      {
        "device_id": "10170206",
        "location": "B23.215B",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:30 GMT",
        "value": 1001
      },
      {
        "device_id": "10170004",
        "location": "B23.110",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:51 GMT",
        "value": 1014
      },
      {
        "device_id": "10170304",
        "location": "B23.123",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:48 GMT",
        "value": 1021
      },
      {
        "device_id": "10170209",
        "location": "B23.217B",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:19:40 GMT",
        "value": 953
      },
      {
        "device_id": "10170202",
        "location": "B23.216",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:47 GMT",
        "value": 950
      },
      {
        "device_id": "10170002",
        "location": "B23.115",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:08:04 GMT",
        "value": 943
      },
      {
        "device_id": "10170208",
        "location": "B23.217A",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:51 GMT",
        "value": 835
      },
      {
        "device_id": "10170203",
        "location": "B23.213",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:49 GMT",
        "value": 1015
      },
      {
        "device_id": "10170003",
        "location": "B23.116",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 16:24:14 GMT",
        "value": 915
      },
      {
        "device_id": "10170102",
        "location": "B23.129A",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:46 GMT",
        "value": 754
      },
      {
        "device_id": "10170205",
        "location": "B23.214B",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:23 GMT",
        "value": 854
      },
      {
        "device_id": "10170105",
        "location": "B23.228",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:51 GMT",
        "value": 801
      },
      {
        "device_id": "10170106",
        "location": "B23.229",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:22 GMT",
        "value": 1005
      },
      {
        "device_id": "10170303",
        "location": "B23.104",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:19:23 GMT",
        "value": 907
      },
      {
        "device_id": "10170009",
        "location": "B23.210",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:25 GMT",
        "value": 936
      },
      {
        "device_id": "10170007",
        "location": "B23.211",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:21 GMT",
        "value": 1005
      },
      {
        "device_id": "10170305",
        "location": "B23.126",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:49 GMT",
        "value": 1023
      },
      {
        "device_id": "10170207",
        "location": "B23.215",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:19:21 GMT",
        "value": 707
      },
      {
        "device_id": "10170005",
        "location": "B23.109",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:47 GMT",
        "value": 934
      },
      {
        "device_id": "10170103",
        "location": "B23.129",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:48 GMT",
        "value": 684
      },
      {
        "device_id": "10170204",
        "location": "B23.214",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:01 GMT",
        "value": 1023
      },
      {
        "device_id": "10170307",
        "location": "B23.122",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:39 GMT",
        "value": 930
      },
      {
        "device_id": "10170006",
        "location": "B23.107",
        "sensor_type": "light",
        "timestamp": "Thu, 08 Aug 2013 17:20:48 GMT",
        "value": 946
      }
    ],
    "motion": [
      {
        "device_id": "10170008",
        "location": "B23.212",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:23 GMT",
        "value": 737
      },
      {
        "device_id": "10170302",
        "location": "B23.105B",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:47 GMT",
        "value": 735
      },
      {
        "device_id": "10170005",
        "location": "B23.109",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:52 GMT",
        "value": 750
      },
      {
        "device_id": "10170308",
        "location": "B23.120",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:07 GMT",
        "value": 753
      },
      {
        "device_id": "10170104",
        "location": "B23.230",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:49 GMT",
        "value": 744
      },
      {
        "device_id": "10170202",
        "location": "B23.216",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:53 GMT",
        "value": 760
      },
      {
        "device_id": "10170206",
        "location": "B23.215B",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:30 GMT",
        "value": 740
      },
      {
        "device_id": "10170004",
        "location": "B23.110",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:51 GMT",
        "value": 739
      },
      {
        "device_id": "10170304",
        "location": "B23.123",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:48 GMT",
        "value": 740
      },
      {
        "device_id": "10170209",
        "location": "B23.217B",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:19:40 GMT",
        "value": 747
      },
      {
        "device_id": "10170002",
        "location": "B23.115",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:08:04 GMT",
        "value": 1015
      },
      {
        "device_id": "10170208",
        "location": "B23.217A",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:51 GMT",
        "value": 731
      },
      {
        "device_id": "10170203",
        "location": "B23.213",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:49 GMT",
        "value": 735
      },
      {
        "device_id": "10170003",
        "location": "B23.116",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 16:24:14 GMT",
        "value": 732
      },
      {
        "device_id": "10170102",
        "location": "B23.129A",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:53 GMT",
        "value": 732
      },
      {
        "device_id": "10170205",
        "location": "B23.214B",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:23 GMT",
        "value": 1023
      },
      {
        "device_id": "10170105",
        "location": "B23.228",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:51 GMT",
        "value": 749
      },
      {
        "device_id": "10170106",
        "location": "B23.229",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:22 GMT",
        "value": 744
      },
      {
        "device_id": "10170303",
        "location": "B23.104",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:19:23 GMT",
        "value": 752
      },
      {
        "device_id": "10170009",
        "location": "B23.210",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:25 GMT",
        "value": 738
      },
      {
        "device_id": "10170007",
        "location": "B23.211",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:21 GMT",
        "value": 747
      },
      {
        "device_id": "10170307",
        "location": "B23.122",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:39 GMT",
        "value": 742
      },
      {
        "device_id": "10170305",
        "location": "B23.126",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:49 GMT",
        "value": 750
      },
      {
        "device_id": "10170207",
        "location": "B23.215",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:19:21 GMT",
        "value": 743
      },
      {
        "device_id": "10170103",
        "location": "B23.129",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:48 GMT",
        "value": 752
      },
      {
        "device_id": "10170204",
        "location": "B23.214",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:01 GMT",
        "value": 742
      },
      {
        "device_id": "10170006",
        "location": "B23.107",
        "sensor_type": "motion",
        "timestamp": "Thu, 08 Aug 2013 17:20:48 GMT",
        "value": 743
      }
    ]
  }
}
	'''

	#return jsonify(data={'motion':motion, 'light':light})

def get_data(url):
	data = json.load(urllib2.urlopen(url))
	
	cleaned_data = []
	for row in data:
		firefly_time = datetime.fromtimestamp(row['timestamp']/1000).date()
		today_time = datetime.today().date()
		if today_time == firefly_time and row['device_id'] != "test" and row['device_id'] != "test-device" and row['device_id'] != "0":
			if mapping_table.has_key(row['device_id']):
				row['timestamp'] = datetime.fromtimestamp(row['timestamp']/1000)
				row['location'] = mapping_table[row['device_id']][2]
				cleaned_data.append(row)
	cleanend_data = sorted(cleaned_data, key=lambda tup: tup["device_id"]) 
	return cleaned_data
def temp_data(): 
	url = 'http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/temp/json'
	data = get_data(url)
	return data
def digital_temp_data():
	url = 'http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/digital_temp/json'
	data = get_data(url)
	return data
def light_data(): 
	url = 'http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/light/json'
	data = get_data(url)
	return data
def pressure_data():
	url = 'http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/pressure/json'
	ddata = get_data(url)
	return data
def humidity_data():
	url = 'http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/humidity/json'
	data = get_data(url)
	return data 
def motion_data(): 
	url = 'http://cmu-sensor-network.herokuapp.com/lastest_readings_from_all_devices/motion/json'
	data = get_data(url)
	return data
@views.route("/")
def home():
	return render_template("problem_map.html")

@views.route("/about")
def about():
	return render_template("sweet_building_greeter.html")

@views.route("/transportation")
def transportation():
	return render_template("transportation.html")
