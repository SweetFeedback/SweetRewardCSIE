from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc


import os, sys	
path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sweet/')
sys.path.append(path)

from model import app, db
from api import api
from views import views


app.register_blueprint(api)
app.register_blueprint(views)

port = 1234

if __name__ == "__main__":
    #app.run(debug=True)
    if len(sys.argv) > 1 and sys.argv[1] == "experiment": 
    	port = 9527
    if len(sys.argv) > 1 and sys.argv[1] == "production":
        port = 5566
    if len(sys.argv) > 1 and sys.argv[1] == "development":
        port = 1234
    port = int(os.environ.get('PORT', port))
    app.run(host='0.0.0.0', port=port, debug=True)
