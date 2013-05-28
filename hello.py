from flask import Flask, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from model import app, db
import config

@app.route("/hello")
def hello():
        return "Hello World!"

@app.route("/beauty")
def beauty():
	return render_template("index.html")

@app.route("/")
def home():
	return render_template("home.html")

### worker part ###
@app.route("/test")
def yo(x=16, y=16):
	x = int(request.args.get("x", x))
	y = int(request.args.get("y", y))
	res = add.apply_async((x, y))
	return res.task_id

@app.route("/test/result/<task_id>")
def show_result(task_id):
    retval = add.AsyncResult(task_id).get(timeout=5.0)
    return repr(retval)
###

@app.route("/reports")
def show_reports():
	from model import Problem
	problems = Problem.query.all()
	return jsonify(data=[i.serialize for i in problems])

@app.route("/members")
def list_members():
	from model import Member
	members = Member.query.all()
	return jsonify(data=[i.serialize for i in members])

# going to insert window_log data 
@app.route("/window_log/insert", methods=['GET', 'POST'])
def insert_window_log():
	from model import Window, WindowIndex
	location_id = request.args.get("location_id", -1)
	window_id = request.args.get("window_id", -1)
	state = request.args.get("state", -1)

	window_log = Window(location_id, window_id, state)
	db.session.add(window_log)
	db.session.commit()
	
	indexs = db.session.query(WindowIndex).filter_by(window_id=window_id).first()
	print indexs
	if indexs is None:
		window_index = WindowIndex(window_log.log_id, window_log.location_id, window_log.window_id, window_log.state, window_log.timestamp)
		db.session.add(window_index)
		db.session.commit()
	else:
		indexs.log_id = window_log.log_id
		indexs.location_id = window_log.location_id
		indexs.state = window_log.state
		indexs.timestamp = window_log.timestamp
		db.session.commit()
		print "update records"
	
	print location_id, window_id, state
	return ""
# show all the data from extended windows data
@app.route("/window_log")
def get_all_extended_window_data():
	from model import Window
	window_log = Window.query.filter(Window.window_id == 1).order_by(desc(Window.timestamp)).all();
	#print window_log.log_id
	#for i in range(len(window_log)):
	#	print window_log[i].log_id
	#print window_log
	#return " " + str(window_log.log_id) + " " +  str(window_log.state) + " " +str(window_log.timestamp)
	return jsonify(data=[i.serialize for i in window_log])
@app.route("/window_index")
def get_window_data_index():
	from model import WindowIndex
	window_indexs = WindowIndex.query.all()
	return jsonify(data=[i.serialize for i in window_indexs])

if __name__ == "__main__":
    app.run(debug=True)
