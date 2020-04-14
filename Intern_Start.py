import os
import time
import filecmp

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
	os.system("sudo bluetoothctl agent off")
	os.system("sudo bluetoothctl agent NoInputNoOutput")
	os.system("sudo bluetoothctl power on")
	os.system("sudo bluetoothctl discoverable on")
	os.system("sudo bluetoothctl pairable on")
	os.system(cmd)

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
		["python-gtk2","install"],
		["pi-bluetooth","install"]]

def checkPipInstallation():
	try:
		import evdev
	except ImportError:
		return False
	return True

def runDependenciesInstallation():
	os.system("sudo apt-get update")
	os.system("sudo apt-get upgrade")
	os.system("sudo apt-get install python-gobject bluez bluez-tools bluez-firmware python-bluez python-dev python-pip python-rpi.gpio screen python-gtk2 pi-bluetooth")

def runPipDependenciesInstallation():
	os.system("sudo pip install evdev")

def checkFiles():
	dir_path = os.path.dirname(os.path.abspath(__file__))
	dir_path = dir_path + "/Subprograms/main.conf"
	if os.path.isfile("/etc/dbus-1/system.d/org.yatbz.dbusbtkeyboardgpioservice.conf") and filecmp.cmp("/etc/bluetooth/main.conf", dir_path):
		return True
	else:
		return False

def copyFiles():
	dir_path = os.path.dirname(os.path.abspath(__file__))
	dir_path = dir_path + "/Subprograms/org.yatbz.dbusbtkeyboardgpioservice.conf"
	os.system("sudo cp " + dir_path + " /etc/dbus-1/system.d/org.yatbz.dbusbtkeyboardgpioservice.conf")
	dir_path = os.path.dirname(os.path.abspath(__file__))
        dir_path = dir_path + "/Subprograms/main.conf"
	os.system("sudo cp -f " + dir_path + " /etc/bluetooth/main.conf")

def checkInstallationRun():
	install = False
	print("Checking dependencies")
	if not(checkInstallation()):
		runDependenciesInstallation()
		install = True
	if not(checkPipInstallation()):
		runPipDependenciesInstallation()
		install = True
	if not(checkFiles()):
		 copyFiles()
		 install = True
	return install

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
