from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
import os
import json
from datetime import date, datetime
import time
import pandas_highcharts

application = Flask(__name__)


def db_connection():
	db = mysql.connector.connect( host = 'comp4442-groupproj.cmwdjsysdln7.us-east-1.rds.amazonaws.com',
	user = 'admin',
	port = '3306',
	database = 'comp4442_project',
	passwd = 'comp4442password')
	return db

db = db_connection()
cur = db.cursor()

@application.route('/list')
def listAllDrivers():
    pwd = os.path.abspath(os.getcwd())
    record_path = os.path.join(pwd, 'SparkAggregatedData')
    res = []
    for filename in os.listdir(record_path):
        f = os.path.join(record_path, filename)
        with open(f) as file:
            lines = file.readlines()
            for i in lines:
                i = i.replace("(","").replace(")","").replace(" ","").replace("'", "").replace("\n","")
                res.append(i.split(","))
            return render_template("list.html", res = res)


@application.route('/')
def home():
    return render_template('home.html')

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

@application.route('/data/<driverid>')
def getData(driverid):
    getTimeAndSpeed = "SELECT speed, time, isOverspeed FROM realtime_records WHERE driverId='{0}' ORDER BY time ASC".format(driverid)
    cur.execute(getTimeAndSpeed)
    records = cur.fetchall()
    res = []
    if len(records) != 0:
        for record in records:
            res.append([record[0], record[1], record[2]])
        return json.dumps(res, default=json_serial)

@application.route('/chart/<driverid>')
def genChart(driverid):
    getTimeAndSpeed = "SELECT speed, time, isOverspeed FROM realtime_records WHERE driverId='{0}' ORDER BY time ASC".format(driverid)
    cur.execute(getTimeAndSpeed)
    records = cur.fetchall()
    res = []
    if len(records) != 0:
        for record in records:
            res.append(json.dumps([record[0], datetime.timestamp(record[1]), record[2]]))
    
    return render_template("chart.html", driverid=driverid, results=res)

@application.route('/list/<driverid>')
def listDriver(driverid):
    pwd = os.path.abspath(os.getcwd())
    record_path = os.path.join(pwd, 'SparkAggregatedData')
    res = []

    for filename in os.listdir(record_path):
        f = os.path.join(record_path, filename)
        with open(f) as file:
            lines = file.readlines()
            for i in lines:
                i = i.replace("(","").replace(")","").replace(" ","").replace("'", "").replace("\n","")
                if driverid in i:
                    print(i)
                    res.append(i.split(","))
                    return render_template("listADriver.html", res = res, driverid = driverid)
            return "ERROR"

if __name__ == '__main__':
	application.run(port=5050, debug=True)