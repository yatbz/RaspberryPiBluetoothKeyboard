import os
import Intern_Start as IS
import zmq
import time

if (IS.checkInstallationRun()):
	print("Dependencies installed or configfile updated.")
	print("Please start script again")
else:
	print("Starting GPIO reading")
	IS.generateBluetoothServer()
	IS.generateDBusServer(False)
	IS.waitingForKeyboard()
	already_started = False
	print("Waiting for connection")

	context = zmq.Context()
	receiver = context.socket(zmq.PULL)
	receiver.connect("tcp://127.0.0.1:5555")
	while True:
		print("-> Waiting for message from DBusServer")
		message = (receiver.recv()).decode("utf-8")
        	if ((message == "Connected") and not(already_started):
                	print("Connected")
                	IS.generateLiveKeyboard()
                	already_started = True
                	print("Transmitting GPIO Keys started")
		while True:
        		if (not(IS.checkBluetoothConnection()) and already_started):
				print("Connection closed")
				already_started = False
				print("Restarting DBusServer")
				print(" - Stopping DBusServer")
				os.system("sudo screen -XS DBusServer quit")
				IS.generateDBusServer(True)
				print("Waiting for connection")
				break
			time.sleep(0.5)

