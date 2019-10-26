#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import os
import sys
from sercom.sercom import SerCom

PIN = 10

def shutdown():
	os.system("killall --wait retroarch mupen64plus emulationstation")
	os.system("sudo shutdown -h now")

# wait for the sercom service to start
time.sleep(2)

# connect to MCU and enable shutdown
sercom = SerCom();

if (sercom.connect() == False):
	print "Cannot connect to MCU!"
	exit(1)

if (sercom.enable_shutdown(True) == False):
	print "Cannot set safe shutdown!"
	exit(2)
	
sercom.close()

# listen to shutdown signal from Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

while (True):
	GPIO.setup(PIN, GPIO.IN)
	
	if (GPIO.input(PIN) == 0):
		shutdown()
		
		GPIO.cleanup()
		exit()
	
	time.sleep(0.5)