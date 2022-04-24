import pandas as pd
import os
import time
import mysql.connector
import json
import random

import sqlalchemy
database_username = 'admin'
database_password = 'comp4442password'
database_ip       = 'comp4442-groupproj.cmwdjsysdln7.us-east-1.rds.amazonaws.com'
database_name     = 'comp4442_project'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))

pwd = os.path.abspath(os.getcwd())

record_path = os.path.join(pwd, 'detail_records')

def db_connection():
	db = mysql.connector.connect( host = 'comp4442-groupproj.cmwdjsysdln7.us-east-1.rds.amazonaws.com',
	user = 'admin',
	port = '3306',
	database = 'comp4442_project',
	passwd = 'comp4442password')
	return db

db = db_connection()

header=['driverID', 'carPlateNumber', 'latitude', 'longtitude', 'speed', 'direction', 'siteName', 'time', 'isRapidlySpeedup', 'isRapidlySlowDown', 'isNeutralSlide', 'isNeutralSlideFinished', 'neutralSlideTime', 'isOverspeed', 'isOverspeedFinished', 'overspeedTime', 'isFatigueDriving', 'isHthrottleStop', 'isOilLeak']

for filename in os.listdir(record_path):
    f = os.path.join(record_path, filename)
    if os.path.isfile(f):
        df = pd.read_csv(f, names=header , index_col=False)
        df["time"] = pd.to_datetime(pd["time"])

        df.to_sql(con=database_connection, name='detail_records', index=False, if_exists='append')
