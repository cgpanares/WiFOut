#!/usr/bin/env python
from flask import Flask
from flaskext.mysql import MySQL
import os
import datetime
import time
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
dateToday.append(today)

dateYear = []
year = datetime.date.today().year
dateYear.append(str(year))

dateMonth = []
monthz = datetime.date.today()
month = monthz.strftime("%B")
dateMonth.append(str(month))

dateDay = []
day = datetime.date.today().day
dateDay.append(str(day))

weeknumber = datetime.date.today().isocalendar()[1]


def reportQuery():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from reports ORDER BY dateOfProcess DESC")
	result_reports = cursor.fetchall()

	return result_reports
	cursor.close()
	conn.close()

def reportQueryD():
	conn = mysql.connect()
	cursor = conn.cursor()
	aDate = dateToday[0]

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from DailyCount WHERE dateDaily = %s ORDER BY dateDaily DESC", (aDate))
	result_reportsD = cursor.fetchall()

	return result_reportsD
	cursor.close()
	conn.close()

def reportQueryW():
	conn = mysql.connect()
	cursor = conn.cursor()
	wDate = weeknumber

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from WeeklyCount WHERE dateWeekly = %s ORDER BY dateWeekly DESC", (wDate))
	result_reportsW = cursor.fetchall()

	return result_reportsW
	cursor.close()
	conn.close()

def reportQueryM():
	conn = mysql.connect()
	cursor = conn.cursor()
	mDate = dateMonth[0]

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from MonthlyCount WHERE dateMonthly = %s ORDER BY dateMonthly DESC", (mDate))
	result_reportsM = cursor.fetchall()

	return result_reportsM
	cursor.close()
	conn.close()

def reportQueryY():
	conn = mysql.connect()
	cursor = conn.cursor()

	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from YearlyCount ORDER BY dateYearly DESC")
	result_reportsY = cursor.fetchall()

	return result_reportsY
	cursor.close()
	conn.close()
