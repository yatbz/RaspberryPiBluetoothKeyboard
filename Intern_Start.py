import os
import time

def generateBluetoothServer():
	print("Generating specialized Bluetooth Server")
	os.system("sudo /etc/init.d/bluetooth stop")
	os.system("sudo screen -d -m -S BluetoothServer bash -c '/usr/sbin/bluetoothd --nodetach --debug -p time'")

def generateDBusServer(restart):
	if (checkDBusServer()):
		print("Stopping previous started DBusServer")
		os.system("sudo screen -XS DBusServer quit")
	if not(restart):
		print("Generating DBusServer")
	else:
		print(" - Generating DBusServer")
	dir_path = os.path.dirname(os.path.abspath(__file__))
	cmd = "sudo screen -d -m -S DBusServer bash -c 'sudo python "
	cmd = cmd + dir_path + "/Subprograms/btk_server.py'"
	os.system("sudo hciconfig hcio up")
	os.system("sudo bluetoothctl discoverable on")
	os.system("sudo bluetoothctl pairable on")
	os.system(cmd)
	os.system("sudo hciconfig hcio class 0x002540")
	os.system("sudo hciconfig hcio name ScrollingPedal")

def checkBluetoothConnection():
	hcitoolconOutput = os.popen("hcitool con").read()
	hcitoolconOutputArray = hcitoolconOutput.split("\n",1)
	if not(hcitoolconOutputArray[1] == ''):
		return True
	else:
		return False

def generateGPIOKeyConverter():
	print("Generating GPIO to Key Converter")
	dir_path = os.path.dirname(os.path.abspath(__file__))
	cmd = "sudo screen -d -m -S GPIOServer bash -c 'sudo python "
	cmd = cmd + dir_path + "/Subprograms/GPIO_Key.py'"
	os.system(cmd)

def generateLiveKeyboard():
	print("Generating live Keyboard")
	dir_path = os.path.dirname(os.path.abspath(__file__))
        cmd = "sudo screen -d -m -S KeyboardServer bash -c 'sudo python "
        cmd = cmd + dir_path + "/Subprograms/kb_client.py'"
        os.system(cmd)

def checkDBusServer():
	screenList = os.popen("sudo screen -ls").read()
	if ("DBusServer" in screenList):
		return True
	else:
		return False

def checkInstallation():
	installationList = giveInstallationList()
	dependenciesList = generateDependenciesList()
	for i in range(0,len(dependenciesList),1):
		if not(dependenciesList[i] in installationList):
			return False
	return True

def giveInstallationList():
	installedDependenciesStringRaw = os.popen("dpkg --get-selections").read()
	installedDependenciesArrayRaw = installedDependenciesStringRaw.split("\n",-1)
	tList = [None]
	for i in range(0,len(installedDependenciesArrayRaw),1):
		tList.extend(installedDependenciesArrayRaw[i].split("\t",-1))
	tList = filter(None, tList)
	finalList = [None]
	for i in range(0,len(tList),2):
		InternList = [tList[i], tList[i+1]]
		finalList.append(InternList)
	finalList = filter(None, finalList)
	return finalList

def generateDependenciesList():
	return [["python-gobject","install"],
		["bluez","install"],
		["bluez-tools","install"],
		["bluez-firmware","install"],
		["python-bluez","install"],
		["python-dev","install"],
		["python-pip","install"],
		["python-rpi.gpio","install"],
		["screen","install"],
		["python-gtk2","install"]]

def checkPipInstallation():
	try:
		import evdev
	except ImportError:
		return False
	return True

def runDependenciesInstallation():
	os.system("sudo apt-get update")
	os.system("sudo apt-get upgrade")
	os.system("sudo apt-get install python-gobject bluez bluez-tools bluez-firmware python-bluez python-dev python-pip python-rpi.gpio screen python-gtk2")

def runPipDependenciesInstallation():
	os.system("sudo pip install evdev")

def checkDBusFile():
	if os.path.isfile("/etc/dbus-1/system.d/org.yaptb.btkbservice.conf"):
		return True
	else:
		return False

def copyDBusFile():
	dir_path = os.path.dirname(os.path.abspath(__file__))
	dir_path = dir_path + "/Subprograms/org.yaptb.btkbservice.conf"
	os.system("sudo cp " + dir_path + " /etc/dbus-1/system.d/org.yaptb.btkbservice.conf")

def checkInstallationRun():
	print("Checking dependencies")
	if not(checkInstallation()):
		runDependenciesInstallation()
	if not(checkPipInstallation()):
		runPipDependenciesInstallation()
	if not(checkDBusFile()):
		 copyDBusFile()

def waitingForKeyboard():
	print("Waiting for Keyboard")
	have_dev = False
	while have_dev == False:
		if os.path.isfile("/dev/input/event0"):
			print("found a keyboard")
			have_dev = True
		else:
			print("Keyboard not found, waiting 3 seconds and retrying")
			time.sleep(3)

def sendString(StringToSend):
	dir_path = os.path.dirname(os.path.abspath(__file__))
	cmd = "python " + dir_path + "/Subprograms/send_string.py " + StringToSend[1]
	os.system(cmd)
	print("String send")
