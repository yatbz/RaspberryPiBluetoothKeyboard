import os
import Intern_Start as IS
import sys

if (len(sys.argv) < 2):
	print("No string to send provided")
else:
	IS.checkInstallationRun()
	IS.generateBluetoothServer()
	IS.generateDBusServer(False)
	print("Waiting for connection")
	while True:
        	if IS.checkBluetoothConnection():
                	print("Connected")
                	IS.sendString(sys.argv)
			break

	os.system("sudo screen -XS DBusServer quit")
	print("Connection closed")

