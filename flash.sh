#!/bin/bash

port=/dev/ttyACM0
scriptdir="/home/pi/daddelkischde2/"

stop_service()
{
	service=$1
	status=$(systemctl is-active $service.service)

	if [[ $status = "active" ]];
	then
		echo "Stopping $service service..."
		sudo systemctl stop $service.service
	fi
}

start_service()
{
	service=$1

	echo "Starting $service service..."
	sudo systemctl start $service.service
}

stop_service dk2_fan_control
stop_service dk2_batmon
stop_service dk2_safe_shutdown
stop_service dk2_sercom_proxy

echo "Resetting..."
python ${scriptdir}reset.py $port

echo "Waiting 3 seconds for bootloader..."
sleep 3

echo "Flashing..."
avrdude -v -p atmega32u4 -c avr109 -P $port -b 57600 -D -U flash:w:${scriptdir}firmware/daddelkischde_mcu.ino.hex:i

echo "Waiting 20 seconds for reboot to finish, please be patient and don't cancel..."
sleep 20

echo "Restarting services..."
start_service dk2_sercom_proxy
start_service dk2_fan_control
start_service dk2_batmon
start_service dk2_safe_shutdown
