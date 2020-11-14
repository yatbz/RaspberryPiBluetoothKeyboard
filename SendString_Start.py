import os
import Intern_Start as IS
import sys

if (len(sys.argv) < 2):
	print("No string to send provided")
else:
	if (IS.checkInstallationRun()):
		print("Dependencies installed or configfile updated.")
		print("Please start script again")
	else:
		print("Please disconnect all bluetoothdevices first and connect if required from console")
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

