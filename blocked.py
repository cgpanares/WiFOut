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


def blocked():
	conn = mysql.connect()
	cursor = conn.cursor()
	cursor2 = conn.cursor()

	cursor2 = conn.cursor(pymysql.cursors.DictCursor)
	cursor2.execute("SELECT * from tempChannel")
	channelq = cursor2.fetchone()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from blocked WHERE channelNumB = %s ORDER BY blockedDate", channelq["channelNumb"])
	result_blocked = cursor.fetchall()

	return result_blocked, channelq
	cursor.close()
	cursor2.close()
	conn.close()

def curChannel():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT channelNumb from tempChannel")
	channelD = cursor.fetchone()


	return channelD
	cursor.close()
	conn.close()

def blockedAgain():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from blocked ORDER BY blockedDate")
	resultsb = cursor.fetchall()

	return resultsb
	cursor.close()
	conn.close()		



	    	


	
