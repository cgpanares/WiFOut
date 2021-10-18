import os
import gc
import subprocess
import subprocess32
import sys
import threading
import thread
import logging
import socket
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def auto_install():
    		print("Just installing required modules")
    		print("if they do not already exist")
		os.system(" pip install flask-mysql ")
		os.system(" pip install wtforms ")
		os.system(" pip install flask_wtf ")
		os.system(" pip install pyric ")
		os.system(" pip install wifi ")
		os.system(" dpkg -i ngrok-beta-linux-amd64.deb ")

		sys.exit("\nRequirements installed.\n")


try:
	from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify, send_file
	from flaskext.mysql import MySQL
	from flask_wtf import Form
	from wtforms import *
	from functools import wraps
	from wtforms.validators import *
	from werkzeug import generate_password_hash, check_password_hash
	from socket import *
	from multiprocessing import Process, current_process
except ImportError:
	auto_install()


from scan2 import search, searchMore, searchMore2
from allowed import allowed
from blocked import blocked, curChannel, blockedAgain
from reports import reportQuery, reportQueryD, reportQueryW, reportQueryM, reportQueryY
from searchDate import datePickerD, datePickerD2, datePickerW, datePickerM
from blockScript import blockIt

import pymysql
import datetime
import time

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'wifout'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


app.secret_key = "super secret key"

dateToday = []
today = datetime.date.today()
dateToday.append(str(today))

dateYear = []
year = datetime.date.today().year
dateYear.append(str(year))

dateMonth = []
monthz = datetime.date.today()
month = monthz.strftime("%B")
dateMonth.append(str(month))

dateMonthandYearD = []
monthY = datetime.date.today()
yearM = monthY.strftime("%B-%Y")
dateMonthandYearD.append(str(yearM))

dateDay = []
day = datetime.date.today().day
dateDay.append(str(day))

os.environ['TZ'] = 'Asia/Manila'
time.tzset()

weeknumber = datetime.date.today().isocalendar()[1]

timeToday = time.strftime("%I:%M %p", time.gmtime())

switch = True

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('main'))

    return wrap


@app.route("/logout/")
@login_required
def logout():
    time.sleep(5)
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('main'))

@app.route("/", methods = ['GET', 'POST'])
def main():

    error = ''
    try:
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	
        if request.method == "POST":
	   username = request.form['username']
	   password = request.form['password']
	
	   data = cursor.execute("SELECT * FROM credentials WHERE userName = (%s)", (username))
	   data = cursor.fetchone()

           if check_password_hash(data["passWord"],password) == True:
                	session['logged_in'] = True
                	session['username'] = username
			
			flash("You are now logged in")
                	return redirect(url_for("dashboard"))

           else:
                error = "Invalid credentials, try again."
		flash(error)

        gc.collect()

        return render_template("login.html", error = error)

    except Exception as e:
        error = "Invalid credentials, try again."
	flash(error)
        return render_template("login.html", error = error)

##########################################################################

@app.route('/dashboards/', methods = ['GET','POST'])
@login_required
def dashboard():
	dataAllow, dataBlock, essid, address, signals, channel = search()
	addressAlls = searchMore2()
	result_allowed = allowed()
	result_blocked, channelq = blocked()
	dateMonthF, dateYearF = datePickerD()
	aDate = dateToday[0]
	yDate = dateYear[0]
	mDate = dateMonth[0]
	dDate = dateDay[0]
	wDate = weeknumber
	try:
		if request.method == 'POST':
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cellID = request.form.getlist('cell_ID', type=int)
			aDate = dateToday[0]
			yDate = dateYear[0]
			mDate = dateMonth[0]
			dDate = dateDay[0]
			myDate = dateMonthandYearD[0]
			wDate = str(weeknumber)
			dateforD = []
			dateforW = []
			dateforM = []
			dateforY = []
			cursor.execute("SELECT * from DailyCount")
			datesD = cursor.fetchall()
			for g in datesD:
				dateforD.append(str(g["dateDaily"]))
			cursor.execute("SELECT * from WeeklyCount")
			datesW = cursor.fetchall()
			for p in datesW:
				dateforW.append(str(p["dateWeekly"]))
			cursor.execute("SELECT * from MonthlyCount")
			datesM = cursor.fetchall()
			for b in datesM:
				dateforM.append(str(b["dateMonthly"]))
			cursor.execute("SELECT * from YearlyCount")
			datesY = cursor.fetchall()
			for c in datesY:
				dateforY.append(str(c["dateYearly"]))
			bssidD = request.form.getlist('bssidMAC', type=str)
			ssidD = request.form.getlist('ssidName', type=str)
			channelD = request.form.getlist('channelMAC', type=str)
			if request.form['action'] == 'Allow':
				if len(cellID) == 0:
					flash("You need to select a data first!")
					return redirect(url_for('dashboard'))
				else:
					for idS in cellID:
							cursor.execute("INSERT INTO allowed( allowedDate, bssidMAC, channelNum, nameSSID) VALUES (%s, %s, %s, %s)",(aDate, bssidD[idS], channelD[idS], ssidD[idS]))
							cursor.execute("INSERT INTO reports( dateOfProcess, yearOfProcess, monthOfProcess, dayOfProcess, weekNofProcess, timeOfProcess, bssidMACR, ssidNameR, channelR, StatusR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(aDate, yDate, mDate, dDate, wDate, timeToday, bssidD[idS], ssidD[idS], channelD[idS], "Allowed"))
							conn.commit()
					for idS in cellID:
						if aDate not in dateforD:
							cursor.execute("INSERT INTO DailyCount(dateDaily, monthAndYear, AllowedD, BlockedD) VALUES (%s, %s, 1, 0)", (aDate, myDate))
							conn.commit()
						else:
							cursor.execute("UPDATE DailyCount SET AllowedD = AllowedD + 1 WHERE dateDaily = %s", (aDate))
							conn.commit()
						if wDate not in dateforW:
							cursor.execute("INSERT INTO WeeklyCount(dateWeekly, yearOfWeek, AllowedW, BlockedW) VALUES (%s, %s, 1, 0)", (wDate, yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE WeeklyCount SET AllowedW = AllowedW + 1 WHERE dateWeekly = %s", (wDate))
							conn.commit()
						if mDate not in dateforM:
							cursor.execute("INSERT INTO MonthlyCount(dateMonthly, yearOfMonth, AllowedM, BlockedM) VALUES (%s, %s, 1, 0)", (mDate, yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE MonthlyCount SET AllowedM = AllowedM + 1 WHERE dateMonthly = %s", (mDate))
							conn.commit()
						if yDate not in dateforY:
							cursor.execute("INSERT INTO YearlyCount(dateYearly, AllowedY, BlockedY) VALUES (%s, 1, 0)", (yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE YearlyCount SET AllowedY = AllowedY + 1 WHERE dateYearly = %s", (yDate))
							conn.commit()
					if mDate not in dateMonthF and yDate not in dateYearF:
						cursor.execute("INSERT INTO tempDate (monthRecordfromR, yearRecordfromR) VALUES (%s, %s)", (mDate, yDate))
						conn.commit()
						flash("Successfully added to Allowed List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
					else:
						flash("Successfully added to Allowed List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
			#################################################################
			elif request.form['action'] == 'Block':
				if len(cellID) == 0:
					flash("You need to select a data first!")
					return redirect(url_for('dashboard'))
				else:
					for idS in cellID:
							cursor.execute("INSERT INTO blocked( blockedDate, bssidMACB, channelNumB, nameSSIDB) VALUES (%s, %s, %s, %s)",(aDate, bssidD[idS], channelD[idS], ssidD[idS]))
							cursor.execute("INSERT INTO reports( dateOfProcess, yearOfProcess, monthOfProcess, dayOfProcess, weekNofProcess, timeOfProcess, bssidMACR, ssidNameR, channelR, StatusR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(aDate, yDate, mDate, dDate, wDate, timeToday, bssidD[idS], ssidD[idS], channelD[idS], "Blocked"))
							conn.commit()
					for idS in cellID:
						if aDate not in dateforD:
							cursor.execute("INSERT INTO DailyCount(dateDaily, monthAndYear, AllowedD, BlockedD) VALUES (%s, %s, 0, 1)", (aDate, myDate))
							conn.commit()
						else:
							cursor.execute("UPDATE DailyCount SET BlockedD = BlockedD + 1 WHERE dateDaily = %s", (aDate))
							conn.commit()
						if wDate not in dateforW:
							cursor.execute("INSERT INTO WeeklyCount(dateWeekly, yearOfWeek, AllowedW, BlockedW) VALUES (%s, %s, 0, 1)", (wDate, yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE WeeklyCount SET BlockedW = BlockedW + 1 WHERE dateWeekly = %s", (wDate))
							conn.commit()
						if mDate not in dateforM:
							cursor.execute("INSERT INTO MonthlyCount(dateMonthly, yearOfMonth, AllowedM, BlockedM) VALUES (%s, %s, 0, 1)", (mDate, yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE MonthlyCount SET BlockedM = BlockedM + 1 WHERE dateMonthly = %s", (mDate))
							conn.commit()
						if yDate not in dateforY:
							cursor.execute("INSERT INTO YearlyCount(dateYearly, AllowedY, BlockedY) VALUES (%s, 0, 1)", (yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE YearlyCount SET BlockedY = BlockedY + 1 WHERE dateYearly = %s", (yDate))
							conn.commit()
					if mDate not in dateMonthF and yDate not in dateYearF:
						cursor.execute("INSERT INTO tempDate (monthRecordfromR, yearRecordfromR) VALUES (%s, %s)", (mDate, yDate))
						conn.commit()
						flash("Successfully added to Blocked List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
					else:
						flash("Successfully added to Blocked List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
			#################################################################
			elif request.form['action'] == 'Allow Device':
				if len(cellID) == 0:
					flash("You need to select a data first!")
					return redirect(url_for('dashboard'))
				else:
					for idS in cellID:
						checkView = cursor.execute("SELECT * FROM blocked WHERE bssidMACB = (%s)", (bssidD[idS]))
						if int(checkView) > 0:
							cursor.execute("DELETE FROM blocked WHERE bssidMACB = (%s)", (bssidD[idS]))
							cursor.execute("INSERT INTO allowed( allowedDate, bssidMAC, channelNum, nameSSID) VALUES (%s, %s, %s, %s)",(aDate, bssidD[idS], channelD[idS], ssidD[idS]))
							cursor.execute("INSERT INTO reports( dateOfProcess, yearOfProcess, monthOfProcess, dayOfProcess, weekNofProcess, timeOfProcess, bssidMACR, ssidNameR, channelR, StatusR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(aDate, yDate, mDate, dDate, wDate, timeToday, bssidD[idS], ssidD[idS], channelD[idS], "Re-allowed"))
							conn.commit()
						else:
							cursor.execute("INSERT INTO allowed( allowedDate, bssidMAC, channelNum, nameSSID) VALUES (%s, %s, %s, %s)",(aDate, bssidD[idS], channelD[idS], ssidD[idS]))
							cursor.execute("INSERT INTO reports( dateOfProcess, yearOfProcess, monthOfProcess, dayOfProcess, weekNofProcess, timeOfProcess, bssidMACR, ssidNameR, channelR, StatusR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(aDate, yDate, mDate, dDate, wDate, timeToday, bssidD[idS], ssidD[idS], channelD[idS], "Allowed"))
							conn.commit()
					for idS in cellID:
						if aDate not in dateforD:
							cursor.execute("INSERT INTO DailyCount(dateDaily, monthAndYear, AllowedD, BlockedD) VALUES (%s, %s, 1, 0)", (aDate, myDate))
							conn.commit()
						else:
							cursor.execute("UPDATE DailyCount SET AllowedD = AllowedD + 1 WHERE dateDaily = %s", (aDate))
							cursor.execute("UPDATE DailyCount SET BlockedD = BlockedD - 1 WHERE dateDaily = %s", (aDate))
							conn.commit()
						if wDate not in dateforW:
							cursor.execute("INSERT INTO WeeklyCount(dateWeekly, yearOfWeek, AllowedW, BlockedW) VALUES (%s, %s, 1, 0)", (wDate, yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE WeeklyCount SET AllowedW = AllowedW + 1 WHERE dateWeekly = %s", (wDate))
							cursor.execute("UPDATE WeeklyCount SET BlockedW = BlockedW - 1 WHERE dateWeekly = %s", (wDate))

							conn.commit()
						if mDate not in dateforM:
							cursor.execute("INSERT INTO MonthlyCount(dateMonthly, yearOfMonth, AllowedM, BlockedM) VALUES (%s, %s, 1, 0)", (mDate, yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE MonthlyCount SET AllowedM = AllowedM + 1 WHERE dateMonthly = %s", (mDate))
							cursor.execute("UPDATE MonthlyCount SET BlockedM = BlockedM - 1 WHERE dateMonthly = %s", (mDate))
							conn.commit()
						if yDate not in dateforY:
							cursor.execute("INSERT INTO YearlyCount(dateYearly, AllowedY, BlockedY) VALUES (%s, 1, 0)", (yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE YearlyCount SET AllowedY = AllowedY + 1 WHERE dateYearly = %s", (yDate))
							cursor.execute("UPDATE YearlyCount SET BlockedY = BlockedY - 1 WHERE dateYearly = %s", (yDate))
							conn.commit()
					if mDate not in dateMonthF and yDate not in dateYearF:
						cursor.execute("INSERT INTO tempDate (monthRecordfromR, yearRecordfromR) VALUES (%s, %s)", (mDate, yDate))
						conn.commit()
						flash("Successfully added to Allowed List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
					else:
						flash("Successfully added to Allowed List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
			##################################################################
			elif request.form['action'] == 'Block Device':
				if len(cellID) == 0:
					flash("You need to select a data first!")
					return redirect(url_for('dashboard'))
				else:
					for idS in cellID:
						checkView = cursor.execute("SELECT * FROM allowed WHERE bssidMAC = %s", (bssidD[idS]))
						if int(checkView) > 0:
							cursor.execute("DELETE FROM allowed WHERE bssidMAC = (%s)", (bssidD[idS]))
							cursor.execute("INSERT INTO blocked( blockedDate, bssidMACB, channelNumB, nameSSIDB) VALUES (%s, %s, %s, %s)",(aDate, bssidD[idS], channelD[idS], ssidD[idS]))
							cursor.execute("INSERT INTO reports( dateOfProcess, yearOfProcess, monthOfProcess, dayOfProcess, weekNofProcess, timeOfProcess, bssidMACR, ssidNameR, channelR, StatusR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(aDate, yDate, mDate, dDate, wDate, timeToday, bssidD[idS], ssidD[idS], channelD[idS], "Re-blocked"))
							conn.commit()
						else:
							cursor.execute("INSERT INTO blocked( blockedDate, bssidMACB, channelNumB, nameSSIDB) VALUES (%s, %s, %s, %s)",(aDate, bssidD[idS], channelD[idS], ssidD[idS]))
							cursor.execute("INSERT INTO reports( dateOfProcess, yearOfProcess, monthOfProcess, dayOfProcess, weekNofProcess, timeOfProcess, bssidMACR, ssidNameR, channelR, StatusR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(aDate, yDate, mDate, dDate, wDate, timeToday, bssidD[idS], ssidD[idS], channelD[idS], "Blocked"))
							conn.commit()
					for idS in cellID:
						if aDate not in dateforD:
							cursor.execute("INSERT INTO DailyCount(dateDaily, monthAndYear, AllowedD, BlockedD) VALUES (%s, %s, 0, 1)", (aDate, myDate))
							conn.commit()
						else:
							cursor.execute("UPDATE DailyCount SET BlockedD = BlockedD + 1 WHERE dateDaily = %s", (aDate))
							cursor.execute("UPDATE DailyCount SET AllowedD = AllowedD - 1 WHERE dateDaily = %s", (aDate))
							conn.commit()
						if wDate not in dateforW:
							cursor.execute("INSERT INTO WeeklyCount(dateWeekly, yearOfWeek, AllowedW, BlockedW) VALUES (%s, %s, 0, 1)", (wDate, yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE WeeklyCount SET BlockedW = BlockedW + 1 WHERE dateWeekly = %s", (wDate))
							cursor.execute("UPDATE WeeklyCount SET AllowedW = AllowedW - 1 WHERE dateWeekly = %s", (wDate))
							conn.commit()
						if mDate not in dateforM:
							cursor.execute("INSERT INTO MonthlyCount(dateMonthly, yearOfMonth, AllowedM, BlockedM) VALUES (%s, %s, 0, 1)", (mDate, yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE MonthlyCount SET BlockedM = BlockedM + 1 WHERE dateMonthly = %s", (mDate))
							cursor.execute("UPDATE MonthlyCount SET AllowedM = AllowedM - 1 WHERE dateMonthly = %s", (mDate))
							conn.commit()
						if yDate not in dateforY:
							cursor.execute("INSERT INTO YearlyCount(dateYearly, AllowedY, BlockedY) VALUES (%s, 0, 1)", (yDate))
							conn.commit()
						else:
							cursor.execute("UPDATE YearlyCount SET BlockedY = BlockedY + 1 WHERE dateYearly = %s", (yDate))
							cursor.execute("UPDATE YearlyCount SET AllowedY = AllowedY - 1 WHERE dateYearly = %s", (yDate))
							conn.commit()
					if mDate not in dateMonthF and yDate not in dateYearF:
						cursor.execute("INSERT INTO tempDate (monthRecordfromR, yearRecordfromR) VALUES (%s, %s)", (mDate, yDate))
						conn.commit()
						flash("Successfully added to Blocked List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
					else:
						flash("Successfully added to Blocked List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
			##################################################################
			elif request.form['action'] == 'Remove Allow':
				if len(cellID) == 0:
					flash("You need to select a data first!")
					return redirect(url_for('dashboard'))
				else:	
					for idS in cellID:
						cursor.execute("DELETE FROM allowed WHERE bssidMAC = %s", (bssidD[idS]))
						cursor.execute("INSERT INTO reports( dateOfProcess, yearOfProcess, monthOfProcess, dayOfProcess, weekNofProcess, timeOfProcess, bssidMACR, ssidNameR, channelR, StatusR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(aDate, yDate, mDate, dDate, wDate, timeToday, bssidD[idS], ssidD[idS], channelD[idS], "R(Allow)"))
						cursor.execute("UPDATE DailyCount SET AllowedD = AllowedD - 1 WHERE dateDaily = %s", (aDate))
						cursor.execute("UPDATE WeeklyCount SET AllowedW = AllowedW - 1 WHERE dateWeekly = %s", (wDate))
						cursor.execute("UPDATE MonthlyCount SET AllowedM = AllowedM - 1 WHERE dateMonthly = %s", (mDate))
						cursor.execute("UPDATE YearlyCount SET AllowedY = AllowedY - 1 WHERE dateYearly = %s", (yDate))
						conn.commit()
					if mDate not in dateMonthF and yDate not in dateYearF:
						cursor.execute("INSERT INTO tempDate (monthRecordfromR, yearRecordfromR) VALUES (%s, %s)", (mDate, yDate))
						conn.commit()
						flash("Successfully removed from Allowed List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
					else:
						flash("Successfully removed from Allowed List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
			##################################################################
			elif request.form['action'] == 'Remove Block':
				if len(cellID) == 0:
					flash("You need to select a data first!")
					return redirect(url_for('dashboard'))
				else:		
					for idS in cellID:
						cursor.execute("DELETE FROM blocked WHERE bssidMACB = %s", (bssidD[idS]))
						cursor.execute("INSERT INTO reports( dateOfProcess, yearOfProcess, monthOfProcess, dayOfProcess, weekNofProcess, timeOfProcess, bssidMACR, ssidNameR, channelR, StatusR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(aDate, yDate, mDate, dDate, wDate, timeToday, bssidD[idS], ssidD[idS], channelD[idS], "R(Block)"))
						cursor.execute("UPDATE DailyCount SET BlockedD = BlockedD - 1 WHERE dateDaily = %s", (aDate))
						cursor.execute("UPDATE WeeklyCount SET BlockedW = BlockedW - 1 WHERE dateWeekly = %s", (wDate))
						cursor.execute("UPDATE MonthlyCount SET BlockedM = BlockedM - 1 WHERE dateMonthly = %s", (mDate))
						cursor.execute("UPDATE YearlyCount SET BlockedY = BlockedY - 1 WHERE dateYearly = %s", (yDate))
						conn.commit()
					if mDate not in dateMonthF and yDate not in dateYearF:
						cursor.execute("INSERT INTO tempDate (monthRecordfromR, yearRecordfromR) VALUES (%s, %s)", (mDate, yDate))
						conn.commit()
						flash("Successfully removed from Blocked List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
					else:
						flash("Successfully removed from Blocked List!")
						cursor.close()
						conn.close()
						return redirect(url_for('dashboard'))
			##################################################################
			elif request.form['action'] == 'Channel 1':
					channelF = 1
					cursor.execute("UPDATE tempChannel SET channelNumb = %s WHERE channel_ID = 0", (channelF))
					conn.commit()
					flash("Successfully changed the channel!")
					cursor.close()
					conn.close()
					return redirect(url_for('dashboard'))
			##################################################################
			elif request.form['action'] == 'Channel 6':
					channelF = 6
					cursor.execute("UPDATE tempChannel SET channelNumb = %s WHERE channel_ID = 0", (channelF))
					conn.commit()
					flash("Successfully changed the channel!")
					cursor.close()
					conn.close()
					return redirect(url_for('dashboard'))
			##################################################################
			elif request.form['action'] == 'Channel 11':
					channelF = 11
					cursor.execute("UPDATE tempChannel SET channelNumb = %s WHERE channel_ID = 0", (channelF))
					conn.commit()
					flash("Successfully changed the channel!")
					cursor.close()
					conn.close()
					return redirect(url_for('dashboard'))
			##################################################################
		elif request.method == 'GET':
			return render_template("dashboard.html", dataAllow = dataAllow, dataBlock = dataBlock, essid = essid, address = address, signals = signals, channel = channel, result_allowed = result_allowed, result_blocked = result_blocked, channelq = channelq, aDate = aDate, addressAlls = addressAlls)

	except Exception as e:
	    return render_template("500.html", error = str(e))


########################################################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def page_not_found(e):
    return render_template("405.html")

@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html", error = e)

@app.route("/about/")
def about():
    if session.get('logged_in'):
    	return render_template("about.html")
    else:
	return render_template("aboutM.html")

@app.route("/help/")
def help():
    if session.get('logged_in'):
    	return render_template("help.html")
    else:
        return render_template("helpM.html")

@app.route('/download/')
def download():
	return send_file('./static/WIFOUT-User-Manual.pdf', attachment_filename = 'usermanual.pdf')
    


########################################################################
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=5, max=20)])
    email = TextField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.Length(min=8, max=20),
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice (updated Jan 22, 2015)', [validators.Required()])

class CPasswordForm(Form):
    username = TextField('Username', [validators.Length(min=5, max=20)])
    password = PasswordField('Old Password', [validators.Length(min=8, max=20),
        validators.Required()])
    passwordN = PasswordField('New Password', [validators.Length(min=8, max=20),
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

########################################################################
@app.route("/register/", methods = ['GET', 'POST'])
def register():
    try:
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	form = RegistrationForm(request.form)
	
	if request.method == "POST" and form.validate():
		username = form.username.data
		email = form.email.data
		password = form.password.data
		_hashed_password = generate_password_hash(password)
		x = cursor.execute("SELECT * FROM credentials WHERE userName = (%s)",
                          (username))

		if int(x) > 0:
                	flash("That username is already taken, please choose another")
                	return render_template('register.html', form=form)
		else:
                	cursor.execute("INSERT INTO credentials (userName, passWord, email, tracking) VALUES (%s, %s, %s, %s)",
                          (username, _hashed_password, email, "/"))
                
                	conn.commit()
                	flash("Thanks for registering!")
                	cursor.close()
                	conn.close()
                	gc.collect()

                	return redirect(url_for('main'))

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
########################################################################
@app.route("/changeP/", methods = ['GET', 'POST'])
def changeP():
    try:
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	form = CPasswordForm(request.form)
	
	if request.method == "POST" and form.validate():
		username = form.username.data
		password = form.passwordN.data
		_hashed_password = generate_password_hash(password)
		x = cursor.execute("SELECT * FROM credentials WHERE userName = (%s)",
                          (username))

		if int(x) > 0:
                	cursor.execute("UPDATE credentials SET passWord = %s WHERE userName = %s", (_hashed_password, username))
                
                	conn.commit()
                	cursor.close()
                	conn.close()
			time.sleep(5)
    			session.clear()
                	gc.collect()
			
			flash("Successfully changed the password!")
                	return redirect(url_for('main'))
		else:
			flash("Invalid Username!")
                	return render_template('ChangePassword.html', form=form)

        return render_template("ChangePassword.html", form=form)

    except Exception as e:
        return(str(e))


############# REPORTS #############

@app.route("/reports/", methods = ['GET', 'POST'])
def report():
	result_reports = reportQuery()
	if request.method == 'POST':
		if request.form['actionR'] == 'Show Record':
			conn = mysql.connect()
			cursor = conn.cursor()
			bssidS = request.form['inputforReport']
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * from reports WHERE bssidMACR LIKE '%" + bssidS + "%' OR ssidNameR LIKE '%" + bssidS + "%' ORDER BY dateOfProcess DESC")
			result_search = cursor.fetchall()
			return render_template("SearchedReport.html", result_search = result_search, bssidS = bssidS)
			cursor.close()
			conn.close()
		elif request.form['actionR'] == 'Go Back':	
			return render_template("reports.html", result_reports = result_reports)
	
	elif request.method == 'GET':
		return render_template("reports.html", result_reports = result_reports)

################################################################################################

@app.route("/reportsDaily/", methods = ['GET', 'POST'])
def reportDaily():
	result_reportsD = reportQueryD()
	dateMonthandYearF = datePickerD2()
	if request.method == 'POST':
		if request.form['actionR'] == 'Show Record':
			conn = mysql.connect()
			cursor = conn.cursor()
			bssidS = request.form['inputforReport']
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * from reports WHERE bssidMACR LIKE '%" + bssidS + "%' OR ssidNameR LIKE '%" + bssidS + "%' ORDER BY dateOfProcess DESC")
			result_search = cursor.fetchall()
			return render_template("SearchedReport.html", result_search = result_search, dateMonthandYearF = dateMonthandYearF, bssidS = bssidS)
			cursor.close()
			conn.close()
		elif request.form['actionR'] == "inputDateSubmit": 	
			conn = mysql.connect()
			cursor = conn.cursor()
			dateD = request.form['MonthYear']
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * from DailyCount WHERE monthAndYear LIKE '%" + dateD + "%' ORDER BY dateDaily DESC")
			result_searchDD = cursor.fetchall()
			return render_template("SearchedReportD.html", result_searchDD = result_searchDD, dateMonthandYearF = dateMonthandYearF, dateD = dateD)
			cursor.close()
			conn.close()
		elif request.form['actionR'] == 'Go Back':	
			return render_template("reportsDaily.html", result_reportsD = result_reportsD, dateMonthandYearF = dateMonthandYearF)

	elif request.method == 'GET':
		return render_template("reportsDaily.html", result_reportsD = result_reportsD, dateMonthandYearF = dateMonthandYearF)
################################################################################################

@app.route("/reportsWeekly/", methods = ['GET', 'POST'])
def reportWeekly():
	result_reportsW = reportQueryW()
	dateSearchW = datePickerW()
	if request.method == 'POST':
		if request.form['actionR'] == 'Show Record':
			conn = mysql.connect()
			cursor = conn.cursor()
			bssidS = request.form['inputforReport']
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * from reports WHERE bssidMACR LIKE '%" + bssidS + "%' OR ssidNameR LIKE '%" + bssidS + "%' ORDER BY dateOfProcess DESC")
			result_search = cursor.fetchall()
			return render_template("SearchedReport.html", result_search = result_search, dateSearchW = dateSearchW, bssidS = bssidS)
			cursor.close()
			conn.close()
		elif request.form['actionR'] == "inputYearWSubmit":
			conn = mysql.connect()
			cursor = conn.cursor()
			dateW = request.form['WeekofYear']
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * from WeeklyCount WHERE yearOfWeek LIKE '%" + dateW + "%' ORDER BY dateWeekly DESC")
			result_searchWW = cursor.fetchall()
			return render_template("SearchedReportW.html", result_searchWW = result_searchWW, dateSearchW = dateSearchW, dateW = dateW)
			cursor.close()
			conn.close()
		elif request.form['actionR'] == 'Go Back':	
			return render_template("reportsWeekly.html", result_reportsW = result_reportsW, dateSearchW = dateSearchW)
	
	elif request.method == 'GET':
		return render_template("reportsWeekly.html", result_reportsW = result_reportsW, dateSearchW = dateSearchW)

################################################################################################

@app.route("/reportsMonthly/", methods = ['GET', 'POST'])
def reportMonthly():
	result_reportsM = reportQueryM()
	dateSearchM = datePickerM()
	if request.method == 'POST':
		if request.form['actionR'] == 'Show Record':
			conn = mysql.connect()
			cursor = conn.cursor()
			bssidS = request.form['inputforReport']
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * from reports WHERE bssidMACR LIKE '%" + bssidS + "%' OR ssidNameR LIKE '%" + bssidS + "%' ORDER BY dateOfProcess DESC")
			result_search = cursor.fetchall()
			return render_template("SearchedReport.html", result_search = result_search, dateSearchM = dateSearchM, bssidS = bssidS)
			cursor.close()
			conn.close()
		elif request.form['actionR'] == "inputYearMSubmit":
			conn = mysql.connect()
			cursor = conn.cursor()
			dateM = request.form['MonthofYear']
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * from MonthlyCount WHERE yearOfMonth LIKE '%" + dateM + "%' ORDER BY dateMonthly DESC")
			result_searchMM = cursor.fetchall()
			return render_template("SearchedReportM.html", result_searchMM = result_searchMM, dateSearchM = dateSearchM, dateM = dateM)
			cursor.close()
			conn.close()
		elif request.form['actionR'] == 'Go Back':	
			return render_template("reportsMonthly.html", result_reportsM = result_reportsM, dateSearchM = dateSearchM)
	
	elif request.method == 'GET':
		return render_template("reportsMonthly.html", result_reportsM = result_reportsM, dateSearchM = dateSearchM)

################################################################################################

@app.route("/reportsYearly/", methods = ['GET', 'POST'])
def reportYearly():
	result_reportsY = reportQueryY()
	if request.method == 'POST':
		if request.form['actionR'] == 'Show Record':
			conn = mysql.connect()
			cursor = conn.cursor()
			bssidS = request.form['inputforReport']
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute("SELECT * from reports WHERE bssidMACR LIKE '%" + bssidS + "%' OR ssidNameR LIKE '%" + bssidS + "%' ORDER BY dateOfProcess DESC")
			result_search = cursor.fetchall()
			return render_template("SearchedReport.html", result_search = result_search, dateSearch = dateSearch, bssidS = bssidS)
			cursor.close()
			conn.close()		
		elif request.form['actionR'] == 'Go Back':	
			return render_template("reportsYearly.html", result_reportsY = result_reportsY)
	
	elif request.method == 'GET':
		return render_template("reportsYearly.html", result_reportsY = result_reportsY)

################################################################################################


if __name__ == '__main__':	

	try:
		p1 = Process(name='app', target=app.run, args=())
		p1.start()
		#while p1.is_alive():	
				#blockIt()	
	except (KeyboardInterrupt):
		p1.terminate()
		gc.collect()
		sys.exit(0)
