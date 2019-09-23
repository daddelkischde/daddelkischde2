#!/usr/bin/env python

import socket
import threading
import serial
from sercom_config import *

class SerComProxy():
	def __init__(self):
		self._clients_lock = threading.Lock()
		self._clients = 0
		
		self._serial_lock = threading.Lock()
		self._serial_port = None

	def start(self):
		while True:
			server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			server_socket.bind((TCP_IP, TCP_PORT))
			server_socket.listen(5)
			
			while True:
				# wait for a new connection
				conn, addr = server_socket.accept()

				self._clients_lock.acquire()
				self._clients += 1
				self._clients_lock.release()
				
				thread = threading.Thread(target = self._client_thread, args = (conn,))
				thread.start()
				
			server_socket.close()

	def _serial_connect(self):
		self._serial_port = serial.Serial(
			port = SERIAL_PORT,
			baudrate = 115200,
			timeout = 2,
			parity = serial.PARITY_NONE,
			stopbits = serial.STOPBITS_ONE,
			bytesize = serial.EIGHTBITS
		)
		
	def _serial_disconnect(self):
		self._serial_lock.acquire()
		
		try:
			if (self._serial_port != None):
				self._serial_port.close()
				self._serial_port = None
		finally:
			self._serial_lock.release()

	def _serial_command(self, request, res_data_len):
		self._serial_lock.acquire()
		
		try:
			if (self._serial_port == None):
				self._serial_connect()
				
			if (self._serial_port == None):
				return False
				
			self._serial_port.write(request)
			response = bytearray(self._serial_port.read(3 + res_data_len))
			
			return response
		finally:
			self._serial_lock.release()

	def _client_thread(self, conn):
		while True:
			data = conn.recv(64)
			
			if (not data):
				# client disconnected
				break
				
			data = bytearray(data)
				
			response = self._serial_command(data[1:], data[0])
			
			conn.send(response)

		conn.close()
		
		self._clients_lock.acquire()
		self._clients -= 1
		self._clients_lock.release()
		
		if (self._clients == 0):
			self._serial_disconnect()

if (__name__ == '__main__'):
	sercom_proxy = SerComProxy()
	sercom_proxy.start()
		