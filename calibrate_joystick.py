from sercom.sercom import SerCom
import time
import thread

def wait_thread(message, signal):
	raw_input(message)
	signal.append(None)
	
def user_wait(message, signal):
	thread.start_new_thread(wait_thread, (message, signal,))

sercom = SerCom();

print "Connecting..."

if (sercom.connect() == False):
	exit("Cannot connect!")

x_max = -0xFFFF
x_min = 0xFFFF
y_max = -0xFFFF
y_min = 0xFFFF

signal = []

user_wait("Slowly move the joystick around and into every corner. When the minimum and maximum values don't change anymore, press Enter.\n", signal)

while (True):
	x = sercom.read_joystick_x()
	y = sercom.read_joystick_y()
	
	changed = False
	
	if (x != False):
		if (x > x_max):
			x_max = x
			changed = True
			
		if (x < x_min):
			x_min = x
			changed = True

	if (y != False):
		if (y > y_max):
			y_max = y
			changed = True
			
		if (y < y_min):
			y_min = y
			changed = True
		
	if (changed):
		print "x_min: {0}, x_max: {1}, y_min: {2}, y_max: {3}".format(x_min, x_max, y_min, y_max)

	if (signal):
		break

x_center = 0
y_center = 0

signal = []

user_wait("Now move the joystick to the center position. Then press Enter.\n", signal)

while (True):
	x = sercom.read_joystick_x()
	y = sercom.read_joystick_y()
	
	if (x != False):
		x_center = x
		
	if (y != False):
		y_center = y
		
	if (signal):
		break

print "x_center: {0}, y_center: {1}\n".format(x_center, y_center)

print "Sending calibration data...\n"

if (sercom.write_joystick_calibration(x_min, x_max, x_center, y_min, y_max, y_center) == False):
	print "Error sending calibration data!"
	exit()

print "That's it! Thanks! Don't forget to enable the joystick."