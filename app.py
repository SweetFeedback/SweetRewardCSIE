from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from model import app, db
from api import api
from views import views
from reports import reports
from members import members 
import config, os

app = Flask(__name__)
app.register_blueprint(reports)
app.register_blueprint(api)
app.register_blueprint(views)
app.register_blueprint(members)

if __name__ == "__main__":
    #app.run(debug=True)
    port = int(os.environ.get('PORT', 1234))
    app.run(host='0.0.0.0', port=port, debug=True)
