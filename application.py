from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
import os

application = Flask(__name__)


def db_connection():
	db = mysql.connector.connect( host = 'comp4442-groupproj.cmwdjsysdln7.us-east-1.rds.amazonaws.com',
	user = 'admin',
	port = '3306',
	database = 'comp4442_project',
	passwd = 'comp4442password')
	return db

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
	application.run(port=5000, debug = True)