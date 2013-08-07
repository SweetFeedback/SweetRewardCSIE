from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc


import config, os, sys	
path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'sweet/')
sys.path.append(path)

from model import app, db
from api import api
from views import views
from reports import reports
from members import members 
from bluetooths import bluetooths
from feedbacks import feedbacks

app = Flask(__name__)
app.register_blueprint(reports)
app.register_blueprint(api)
app.register_blueprint(views)
app.register_blueprint(members)
app.register_blueprint(bluetooths)
app.register_blueprint(feedbacks)

if __name__ == "__main__":
    #app.run(debug=True)
    port = int(os.environ.get('PORT', 1234))
    app.run(host='0.0.0.0', port=port, debug=True)
