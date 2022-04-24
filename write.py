import time
import mysql.connector
import json
import random
from datetime import datetime, timedelta

def db_connection():
	db = mysql.connector.connect( host = 'comp4442-groupproj.cmwdjsysdln7.us-east-1.rds.amazonaws.com',
	user = 'admin',
	port = '3306',
	database = 'comp4442_project',
	passwd = 'comp4442password')
	return db

db = db_connection()
cur = db.cursor()
    
def feedToRealtimeTable(t):
    #sql = "SELECT * FROM detail_records WHERE time='{0}'".format(t)
    #cur.execute(sql)
    #records = cur.fetchall()
    #if len(records) != 0:
    #    for record in records:
    #        print(record)
    sql2 = "INSERT INTO realtime_records SELECT * FROM detail_records WHERE detail_records.time='{0}'".format(t)

    cur.execute(sql2)
    db.commit()

experimentTime = datetime(2017, 1, 1, 8, 0, 0)

while True:
    time.sleep(1)
    experimentTime += timedelta(seconds=1)
    inputTime = experimentTime.strftime("%y-%m-%d %H:%M:%S")
    feedToRealtimeTable(experimentTime)