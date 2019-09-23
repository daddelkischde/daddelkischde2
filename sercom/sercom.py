#!/usr/bin/env python

import socket
import sys
from sercom_config import *

class SerCom():
	CMD_HELLO = 0x00
	CMD_LCD_RESET = 0x01
	CMD_LCD_SET_PWM = 0x02
	CMD_LCD_GET_PWM = 0x03
	CMD_LCD_WRITE_REG = 0x04
	CMD_BAT_READ = 0x05
	CMD_SHDN_ENABLE = 0x06
	CMD_FAN_SET_PWM = 0x07
	CMD_FAN_GET_PWM = 0x08
	CMD_JOY_SET_ENABLE = 0x09
	CMD_JOY_GET_ENABLE = 0x0A
	CMD_JOY_X_READ = 0x0B
	CMD_JOY_Y_READ = 0x0C
	CMD_JOY_CALIB_WRITE = 0x0D
	CMD_LOGO_SET_DISPLAY = 0x0E
	CMD_LOGO_GET_DISPLAY = 0x0F
	CMD_REBOOT = 0x10
	CMD_VERSION_GET = 0x11
	CMD_BTN_COMBO_SET = 0x12
	CMD_BTN_COMBO_GET = 0x13
	CMD_BUTTONS_READ = 0x14
	
	RES_OK = 0x00
	RES_NOK = 0x01
	RES_UNKNOWN_CMD = 0x02
	RES_CHECKSUM_ERR = 0x03
	RES_INVALID_PARAMETERS = 0x04
	
	BTN_COMBO_BACKLIGHT_INC = 0x00
	BTN_COMBO_BACKLIGHT_DEC = 0x01
	BTN_COMBO_LCD_RESET = 0x02
	BTN_COMBO_GAMMA_INC = 0x03
	BTN_COMBO_GAMMA_DEC = 0x04
	BTN_COMBO_GAMMA_IDX_INC = 0x05
	BTN_COMBO_GAMMA_IDX_DEC = 0x06
	BTN_COMBO_FAN_ON = 0x07
	BTN_COMBO_FAN_OFF = 0x08
	
	BTN_JOY_UP = 0x00100000
	BTN_JOY_DOWN = 0x00080000
	BTN_JOY_LEFT = 0x00040000
	BTN_JOY_RIGHT = 0x00020000
	BTN_MODE = 0x00010000
	BTN_B = 0x00008000
	BTN_Y = 0x00004000
	BTN_SELECT = 0x00002000
	BTN_START = 0x00001000
	BTN_UP = 0x00000800
	BTN_DOWN = 0x00000400
	BTN_LEFT = 0x00000200
	BTN_RIGHT = 0x00000100
	BTN_A = 0x00000080
	BTN_X = 0x00000040
	BTN_L = 0x00000020
	BTN_R = 0x00000010
	BTN_C = 0x00000008
	BTN_Z = 0x00000004
	BTN_L2 = 0x00000002
	BTN_R2 = 0x00000001

	def __init__(self, debug_output = False):
		self._debug_output = debug_output

	def _format_hex_list(self, res):
		return " ".join("{:02X}".format(c) for c in res)

	def _cmd(self, cmd, data, res_data_len):
		request = [ cmd ] + data
		
		checksum = 0
		
		for c in request:
			checksum += c
			checksum &= 0xFF
			
		request += [ checksum ]

		if (self._debug_output):
			print "request: " + self._format_hex_list(request)

		self._socket.send(bytearray([ res_data_len ] + request))
		
		try:
			response = bytearray(self._socket.recv(64))
		except:
			print "No response received!"
			
			return False
		
		if (len(response) == 0):
			print "No response received!"
			
			return False
		
		if (self._debug_output):
			print "response: " + self._format_hex_list(response)
		
		if (response[0] != request[0]):
			print "Opcode not mirrored! {0:02X} expected, {1:02X} received".format(request[0], response[0])
			
			return False
			
		if (response[1] != self.RES_OK):
			print "Result is not ok: {0:02X}".format(response[1])
			
			return False
			
		checksum = 0
		
		for c in response[:len(response) - 1]:
			checksum += c
			checksum &= 0xFF
			
		if (response[len(response) - 1] != checksum):
			print "Invalid checksum! {0:02X} expected, {1:02X} received".format(checksum, response[len(response) - 1])
			
			return False
			
		return response[2:len(response) - 1]

	def connect(self):
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			self._socket.connect((TCP_IP, TCP_PORT))
		except:
			print "Could not connect to serial proxy!"
			
			return False
		
		result = self._cmd(self.CMD_HELLO, [ 0x13 ], 1)

		if (result == False):
			print "Initialization failed!"
			
			return False
			
		if (result[0] != 0x37):
			print "Wrong replay to 'hello' request!"
			
			return False
			
		return True
		
	def close(self):
		self._socket.close()

	def get_version(self):
		result = self._cmd(self.CMD_VERSION_GET, [], 2)
			
		if (result == False):
			return False
			
		return "{0}.{1}".format(result[0], result[1])

	def lcd_reset(self):
		result = self._cmd(self.CMD_LCD_RESET, [], 0)
			
		if (result == False):
			return False
			
		return True

	def lcd_write_reg(self, reg, data):
		payload = [ reg, len(data) ] + data
		
		while (len(payload) < 30):
			payload += [ 0 ]

		result = self._cmd(self.CMD_LCD_WRITE_REG, payload, 0)
			
		if (result == False):
			return False
			
		return True
		
	def read_battery(self):
		result = self._cmd(self.CMD_BAT_READ, [], 2)
			
		if (result == False):
			return False
			
		battery_raw = (result[0] << 8) + result[1]
		battery = (3.3 / 1024) * 2 * battery_raw

		return round(battery, 2)
		
	def enable_shutdown(self, enabled):
		if (enabled):
			payload = 0x01
		else:
			payload = 0x00
			
		result = self._cmd(self.CMD_SHDN_ENABLE, [ payload ], 0)
		
		if (result == False):
			return False
			
		return True
		
	def set_joystick_enable(self, enabled):
		if (enabled):
			payload = 0x01
		else:
			payload = 0x00
			
		result = self._cmd(self.CMD_JOY_SET_ENABLE, [ payload ], 0)
		
		if (result == False):
			return False
			
		return True
	
	def get_joystick_enable(self):
		result = self._cmd(self.CMD_JOY_GET_ENABLE, [], 1)
		
		if (result == False):
			return False
			
		if (result[0] == 0):
			return False
		
		return True
		
	def read_joystick(self, x):
		if (x):
			cmd = self.CMD_JOY_X_READ
		else:
			cmd = self.CMD_JOY_Y_READ
	
		result = self._cmd(cmd, [], 2)
			
		if (result == False):
			return False
			
		joystick = (result[0] << 8) + result[1]

		return joystick
		
	def read_joystick_x(self):
		return self.read_joystick(True)
		
	def read_joystick_y(self):
		return self.read_joystick(False)
		
	def write_joystick_calibration(self, min_x, max_x, center_x, min_y, max_y, center_y):
		payload = [ (min_x >> 8) & 0xFF, (min_x >> 0) & 0xFF,
					(max_x >> 8) & 0xFF, (max_x >> 0) & 0xFF,
					(center_x >> 8) & 0xFF, (center_x >> 0) & 0xFF,
					(min_y >> 8) & 0xFF, (min_y >> 0) & 0xFF,
					(max_y >> 8) & 0xFF, (max_y >> 0) & 0xFF,
					(center_y >> 8) & 0xFF, (center_y >> 0) & 0xFF ]
		
		result = self._cmd(self.CMD_JOY_CALIB_WRITE, payload, 0)
			
		if (result == False):
			return False
			
		return True
		
	def reboot(self):
		result = self._cmd(self.CMD_REBOOT, [], 0)
			
		if (result == False):
			return False
			
		return True
		
	def set_logo_display(self, display_time):
		payload = [ (display_time >> 8) & 0xFF, (display_time >> 0) & 0xFF ]
		
		result = self._cmd(self.CMD_LOGO_SET_DISPLAY, payload, 0)
			
		if (result == False):
			return False
			
		return True
		
	def get_logo_display(self):
		result = self._cmd(self.CMD_LOGO_GET_DISPLAY, [], 2)
		
		if (result == False):
			return False
			
		return (result[0] << 8) + result[1]
		
	def get_button_names(self):
		buttons = [ [ self.BTN_R2, "R2" ],
					[ self.BTN_L2, "L2" ],
					[ self.BTN_Z, "Z" ],
					[ self.BTN_C, "C" ],
					[ self.BTN_R, "R" ],
					[ self.BTN_L, "L" ],
					[ self.BTN_X, "X" ],
					[ self.BTN_A, "A" ],
					[ self.BTN_RIGHT, "Right" ],
					[ self.BTN_LEFT, "Left" ],
					[ self.BTN_DOWN, "Down" ],
					[ self.BTN_UP, "Up" ],
					[ self.BTN_START, "Start" ],
					[ self.BTN_SELECT, "Select" ],
					[ self.BTN_Y, "Y" ],
					[ self.BTN_B, "B" ],
					[ self.BTN_MODE, "Mode" ],
					[ self.BTN_JOY_RIGHT, "Joystick right" ],
					[ self.BTN_JOY_LEFT, "Joystick left" ],
					[ self.BTN_JOY_DOWN, "Joystick down" ],
					[ self.BTN_JOY_UP, "Joystick up" ] ]
		
		return buttons

	def set_button_combo(self, combo_type, buttons):
		buttons_bmp = 0
		
		for button in buttons:
			buttons_bmp = buttons_bmp | button
	
		payload = [ combo_type, (buttons_bmp >> 24) & 0xFF, (buttons_bmp >> 16) & 0xFF, (buttons_bmp >> 8) & 0xFF, (buttons_bmp >> 0) & 0xFF ]
		
		result = self._cmd(self.CMD_BTN_COMBO_SET, payload, 0)
		
		if (result == False):
			return False
			
		return True
		
	def get_button_combo(self, combo_type):
		result = self._cmd(self.CMD_BTN_COMBO_GET, [ combo_type], 4)
		
		if (result == False):
			return False
			
		buttons_bmp = (result[0] << 24) + (result[1] << 16) + (result[2] << 8) + (result[3] << 0)

		return buttons_bmp
		
	def set_fan(self, fan_on):
		if (fan_on):
			payload = [ 0xFF ]
		else:
			payload = [ 0x00 ]
	
		result = self._cmd(self.CMD_FAN_SET_PWM, payload, 0)
		
		return result
		
	def get_fan(self):
		result = self._cmd(self.CMD_FAN_GET_PWM, [], 1)
		
		if (result == False):
			return False
			
		if (result[0] == 0):
			return False
		
		return True
		
	def read_buttons(self):
		result = self._cmd(self.CMD_BUTTONS_READ, [], 4)
		
		if (result == False):
			return False
			
		return (result[0] << 24) + (result[1] << 16) + (result[2] << 8) + (result[3] << 0)