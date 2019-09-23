#!/usr/bin/python

import sys
from sercom.sercom import SerCom

sercom = SerCom();

if (sercom.connect() == False):
	print("Cannot connect to MCU!")
	
	exit(1)
	
if (len(sys.argv) > 1):
	command = sys.argv[1]
	parameter1 = ""
	
	if (len(sys.argv) > 2):
		parameter1 = sys.argv[2]
	
	if (command == "get_version"):
		print(sercom.get_version())
	
	if (command == "fan_on"):
		sercom.set_fan(True)
	
	if (command == "fan_off"):
		sercom.set_fan(False)
		
	if (command == "get_fan"):
		if (sercom.get_fan() == 0):
			print("off")
		else:
			print("on")
		
	if (command == "set_logo_display"):
		sercom.set_logo_display(int(parameter1))
		
	if (command == "get_logo_display"):
		print(sercom.get_logo_display())
		
	if (command == "set_joystick_enabled"):
		sercom.set_joystick_enable(True)
		
	if (command == "set_joystick_disabled"):
		sercom.set_joystick_enable(False)
		
	if (command == "get_joystick_enabled"):
		if (sercom.get_joystick_enable()):
			print("enabled")
		else:
			print("disabled")
			
	if (command == "get_button_combo"):
		buttons = 0
		
		if (parameter1 == "backlight_inc"):
			buttons = sercom.get_button_combo(sercom.BTN_COMBO_BACKLIGHT_INC)
		elif (parameter1 == "backlight_dec"):
			buttons = sercom.get_button_combo(sercom.BTN_COMBO_BACKLIGHT_DEC)
		elif (parameter1 == "fan_on"):
			buttons = sercom.get_button_combo(sercom.BTN_COMBO_FAN_ON)
		elif (parameter1 == "fan_off"):
			buttons = sercom.get_button_combo(sercom.BTN_COMBO_FAN_OFF)

		if (buttons != 0):
			button_names = sercom.get_button_names()
				
			output = ""
				
			for i in range(0, 21):
				mask = 1 << i
				
				for button_name in button_names:
					if (mask == button_name[0]):
						output += str(i) + "," + button_name[1] + ","
						
						if (buttons & mask == mask):
							output += "on"
						else:
							output += "off"
							
						output += ","
							
			print(output)
		
	if (command == "set_button_combo"):
		combo = -1
		
		if (parameter1 == "backlight_inc"):
			combo = sercom.BTN_COMBO_BACKLIGHT_INC
		elif (parameter1 == "backlight_dec"):
			combo = sercom.BTN_COMBO_BACKLIGHT_DEC
		elif (parameter1 == "fan_on"):
			combo = sercom.BTN_COMBO_FAN_ON
		elif (parameter1 == "fan_off"):
			combo = sercom.BTN_COMBO_FAN_OFF
			
		if (combo >= 0):
			buttons = []
			
			for arg in sys.argv[3:]:
				mask = 1 << int(arg)
				buttons.append(mask)

			sercom.set_button_combo(combo, buttons)
			
	if (command == "reboot"):
		sercom.reboot()
	
sercom.close()
