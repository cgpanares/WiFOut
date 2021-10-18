#!/usr/bin/env python
from flask import Flask
from flaskext.mysql import MySQL
import os
import time
import pymysql
	
mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'wifout'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


def allowed():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor2 = conn.cursor()

	cursor2 = conn.cursor(pymysql.cursors.DictCursor)
	cursor2.execute("SELECT * from tempChannel")
	channelq = cursor2.fetchone()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from allowed WHERE channelNum = %s ORDER BY allowedDate", channelq["channelNumb"])
	result_allowed = cursor.fetchall()

	return result_allowed
	cursor2.close()
	cursor.close()
	conn.close()

	
