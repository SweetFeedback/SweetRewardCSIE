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


app.register_blueprint(api)
app.register_blueprint(views)

port = 5566

if __name__ == "__main__":
    #app.run(debug=True)
    if len(sys.argv) > 1  and sys.argv[1] is "experiment": 
    	port = 9527
    port = int(os.environ.get('PORT', port))
    app.run(host='0.0.0.0', port=port, debug=True)
