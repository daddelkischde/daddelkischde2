#!/usr/bin/env python

# SOURCE: https://github.com/nicholaskell/Arduino_Loader

import serial, sys

serialPort = sys.argv[1]

ser = serial.Serial(
  port=serialPort,
  baudrate=1200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS
)

#ser.close()

#ser.open()

ser.setRTS(True)
ser.setDTR(False)

ser.isOpen()
ser.close()
