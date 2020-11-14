import os
import Intern_Start as IS

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
	while True:
        	if IS.checkBluetoothConnection() and not(already_started):
                	print("Connected")
                	IS.generateLiveKeyboard()
                	already_started = True
                	print("Transmitting GPIO Keys started")
        	elif (not(IS.checkBluetoothConnection()) and already_started):
                	print("Connection closed")
                	already_started = False
                	print("Restarting DBusServer")
                	print(" - Stopping DBusServer")
                	os.system("sudo screen -XS DBusServer quit")
                	IS.generateDBusServer(True)
                	print("Waiting for connection")

