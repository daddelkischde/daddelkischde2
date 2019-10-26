#!/usr/bin/python

import time
import signal
from subprocess import PIPE, Popen
from sercom.sercom import SerCom
from fan_control_config import *

def get_cpu_temperature():
	process = Popen(['vcgencmd', 'measure_temp'], stdout=PIPE)
	output, _error = process.communicate()
	return float(output[output.index('=') + 1:output.rindex("'")])

def end_process(signalnum = None, handler = None):
	global sercom
	sercom.close
	exit(0)

# wait for the sercom service to start
time.sleep(2)

# connect to MCU
sercom = SerCom();

if (sercom.connect() == False):
	print("Cannot connect to MCU!")
	
	exit(1)

signal.signal(signal.SIGTERM, end_process)
signal.signal(signal.SIGINT, end_process)

sercom.set_fan(False)
fan_on = False

while (True):
	temp = get_cpu_temperature()
	fan_on = sercom.get_fan()

	if ((fan_on == False) and (temp >= LIMIT_ON)):
		sercom.set_fan(True)

	if ((fan_on == True) and (temp <= LIMIT_OFF)):
		sercom.set_fan(False)

	time.sleep(MONITOR_INTERVAL)
