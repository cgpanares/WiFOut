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

from flask import Flask, render_template
from flaskext.mysql import MySQL

from scan2 import search, searchMore
from allowed import allowed
from blocked import curChannel, blockedAgain

import pymysql
import datetime
import time

mysql = MySQL()

def blockIt():
    global t
    t = threading.Timer(30.0, blockIt)
    t.daemon = True
    t.start()
    try:
	result_address = allowed()
    	addressAll = searchMore()
    	resultsb = blockedAgain()
    	channelD = curChannel()
    	fChannel = channelD["channelNumb"]
	search()
	searchedDevices = []
	blockedDevices = []
    	for s in addressAll:
		searchedDevices.append(s)

    	for b in resultsb:
		if b["channelNumB"] == fChannel:
			blocksq = b["bssidMACB"]
			if blocksq in searchedDevices:
				blockedDevices.append(str(blocksq.lower()))

    	textFromList = ' '.join(blockedDevices)
    	shpfiles = str(fChannel)
    	print ("List of MAC Addresses for channel: " + shpfiles)
    	print textFromList
	try:
		    os.system('timeout 25 python blockerD.py ' + shpfiles + ' ' + textFromList)
	except subprocess32.TimeoutExpired or InterfaceError or KeyboardInterrupt as e:
		    print ("Ending Thread, starting a new one...")
		    del blockedDevices[:]
    		    del textFromList
		    time.sleep(2)
		    t.cancel()
	finally:
		    print ("Ending Thread, starting a new one...")
		    del blockedDevices[:]
    		    del textFromList
		    time.sleep(2)
		    t.cancel()
    except:
		    time.sleep(2)
		    t.cancel()
