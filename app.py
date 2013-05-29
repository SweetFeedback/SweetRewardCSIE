from flask import Flask, Blueprint, render_template, request, jsonify, json
from celery import Celery 
from tasks import add

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, TIMESTAMP, desc
from model import app, db
from api import api
from views import views
import config


app = Flask(__name__)
#app.config.from_object(settings)
app.register_blueprint(api)
app.register_blueprint(views)


if __name__ == "__main__":
    app.run(debug=True)
