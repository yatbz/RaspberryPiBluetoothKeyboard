import os
import Intern_Start as IS
import sys
import zmq

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

		context = zmq.Context()
		receiver = context.socket(zmq.PULL)
		receiver.connect("tcp://127.0.0.1:5555")
		print("-> Waiting for message from DBusServer")

		message = (receiver.recv()).decode("utf-8")
        	if (message == "Connected"):
                	print(message)
                	IS.sendString(sys.argv)

		os.system("sudo pkill screen")
		print("Connection closed")

