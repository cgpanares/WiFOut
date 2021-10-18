#!/usr/bin/env python
from flask import Flask
from flaskext.mysql import MySQL
import os
import time
import datetime
import pymysql
	
mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'wifout'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

dateToday = []
today = datetime.date.today()
dateToday.append(str(today))

dateSearch = []

dateMonthF = []
dateYearF = []
dateMonthandYearF = []

def datePickerD2():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from tempDate ORDER BY yearRecordfromR DESC")
	dateMonthandYearF = cursor.fetchall()
	return dateMonthandYearF
	cursor.close()
	conn.close()

def datePickerD():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from tempDate ORDER BY yearRecordfromR DESC")
	dateSearchD = cursor.fetchall()
	for row in dateSearchD:
		dateMonthF.append(str(row["monthRecordfromR"]))
		dateYearF.append(str(row["yearRecordfromR"]))
	return dateMonthF, dateYearF
	cursor.close()
	conn.close()

def datePickerW():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from YearlyCount ORDER BY dateYearly DESC")
	dateSearchW = cursor.fetchall()

	return dateSearchW
	cursor.close()
	conn.close()

def datePickerM():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from YearlyCount ORDER BY dateYearly DESC")
	dateSearchM = cursor.fetchall()

	return dateSearchM
	cursor.close()
	conn.close()	
