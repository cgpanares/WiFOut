#!/usr/bin/env python
from flask import Flask
from flaskext.mysql import MySQL
from wifi import Cell
from blocked import curChannel
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

def search():
	conn = mysql.connect()
	dataAllow = []
	dataBlock = []
	channelBlock = []

	essid=[]
	address=[]
	signals=[]
	channel=[]
	
	channelD = curChannel()
    	fChannel = channelD["channelNumb"]


	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("SELECT * from allowed")
	rows1 = cursor.fetchall()
	cursor2 = conn.cursor(pymysql.cursors.DictCursor)
	cursor2.execute("SELECT * from blocked")
	rows2 = cursor2.fetchall()

	for i in rows1:
	  	dataAllow.append(i["bssidMAC"])    
	for j in rows2:
	    	dataBlock.append(j["bssidMACB"])
		channelBlock.append(j["channelNumB"])


	for x in xrange(0,1):
		cell = Cell.all('wlan1')
		for x in xrange(0, len(cell)):
			#if (str(cell[x].address) in dataBlock) and (str(cell[x].channel) not in channelBlock):
				#cursor.execute("UPDATE blocked SET channelNumB = %s WHERE bssidMACB = %s", (str(cell[x].channel), str(cell[x].address)))
				#conn.commit()
			if (str(cell[x].address) not in dataAllow) and (str(cell[x].address) not in dataBlock):
				if str(cell[x].channel) == fChannel:
					essid.append(str(cell[x].ssid))
					address.append(str(cell[x].address))
					signals.append(str(cell[x].signal))
					channel.append(str(cell[x].channel))
	return dataAllow, dataBlock, essid, address, signals, channel


def searchMore():
	addressAll=[]
	channelD = curChannel()
    	fChannel = channelD["channelNumb"]

	for x in xrange(0,1):
		cell = Cell.all('wlan1')
		for x in xrange(0, len(cell)):
			if str(cell[x].channel) == fChannel:
				addressAll.append(str(cell[x].address))
	return addressAll


def searchMore2():
	addressAlls=[]

	for x in xrange(0,1):
		cell = Cell.all('wlan1')
		for x in xrange(0, len(cell)):
				addressAlls.append(str(cell[x].address))
	return addressAlls




