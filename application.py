from flask import Flask, render_template, request
import mysql.connector

application = Flask(__name__)


def db_connection():
	db = mysql.connector.connect( host = 'comp4442-groupproj.cmwdjsysdln7.us-east-1.rds.amazonaws.com',
	user = 'admin',
	port = '3306',
	database = 'comp4442_project',
	passwd = 'comp4442password')
	return db

@application.route('/list')
def list():
    db = db_connection()
    
    cur = db.cursor()
    cur.execute('select * from detail_records')
    res = cur.fetchall()
    for data in res:
        print(data)
    return render_template('list.html', results = res)

@application.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
	application.run(port=5000, debug = True)