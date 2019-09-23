#!/usr/bin/python

import time
import signal
import datetime
import os
from sercom.sercom import SerCom
from subprocess import check_output, call, Popen
from batmon_config import *

def draw_icon(layer, icon):
	Popen(PNGVIEW_PATH + "/pngview -b 0 -l " + str(layer) + " -x " + str(ICON_X) + " -y " + str(ICON_Y) + " " + ICON_PATH + "/" + icon + " &", cwd=os.path.dirname(os.path.realpath(__file__)), shell=True)

def change_icon(percent, icon):
	draw_icon(DISPMANX_BASE_LAYER + percent, icon)

	if (DEBUG_MSG == 1):
		print("Changed battery icon to " + str(percent) + "%")

	out = check_output("ps aux | grep pngview | awk '{ print $2 }'", shell=True)
	nums = out.split('\n')

	# kill the oldest icon
	call("sudo kill " + nums[0], shell=True)

def end_process(signalnum = None, handler = None):
	call("sudo killall pngview", shell=True);
	exit(0)
	
def read_battery(sercom):
	# measure three times and use the average
	battery = (sercom.read_battery() + sercom.read_battery() + sercom.read_battery()) / 3

	return battery

# prepare handlers for process exit
signal.signal(signal.SIGTERM, end_process)
signal.signal(signal.SIGINT, end_process)

# wait for the sercom service to start
time.sleep(2)

# connect to MCU
sercom = SerCom();

if (sercom.connect() == False):
	if (DEBUG_MSG == 1):
		print("Cannot connect to MCU!")
	
	exit(1)

if (CSV_OUT == 1):
	print("#;Timestamp;Date and time;Voltage")

count = 0
current_icon = ""

while True:
	voltage = read_battery(sercom)
	
	if (CSV_OUT == 1):
		print(str(count) + ";" + str(time.time()) + ";" + str(datetime.datetime.now()) + ";" + str(voltage))

	if (voltage != 0):
		# valid reading
		if (DEBUG_MSG == 1):
			print("Battery: " + str(voltage) + " V")

		for volt_step in VOLT_STEPS:
			percent = volt_step[0]
			limit = volt_step[1]
			icon = volt_step[2]
			
			if (voltage > limit):
				if (current_icon != icon):
					change_icon(percent, icon)
					current_icon = icon
					
				break

	count += 1
	time.sleep(REFRESH_RATE)
