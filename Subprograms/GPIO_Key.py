import os
import sys # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import RPi.GPIO as GPIO
import time
import thread

class GPIOClient():
	#------------------>CHANGE HERE<-------------------------#
	GPIOs = [26, 20]
	connectedKeys = [78, 75]
	#GPIO PIN 26 triggers KEYID 78 (KEY_PAGEDOWN)
	#GPIO PIN 20 triggers KEYID 75 (KEY_PAGEUP)
	REPEAT_KEY_DELAY = 0.25
	#------------------>UNTIL HERE<-------------------------#
	def __init__(self):
		self.state=[
                    0xA1, #this is an input report
                    0x01, #Usage report = Keyboard
                    #Bit array for Modifier keys
                    [0, #Right GUI - Windows Key
                     0, #Right ALT
                     0, #Right Shift
                     0, #Right Control
                     0, #Left GUI
                     0, #Left ALT
                     0, #Left Shift
                     0],    #Left Control
                    0x00,   #Vendor reserved
                    0x00,   #rest is space for 6 keys
                    0x00,
                    0x00,
                    0x00,
                    0x00,
                    0x00]
		print "Initializing GPIO"
		GPIO.setmode(GPIO.BCM)
		for i in range(0,len(self.GPIOs), 1):
			GPIO.setup(self.GPIOs[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

		print " - setting up DBus Client"

		self.bus = dbus.SystemBus()
        	self.btkservice = self.bus.get_object('org.yatbz.dbusbtkeyboardgpioservice','/org/yatbz/dbusbtkeyboardgpioservice')
        	self.iface = dbus.Interface(self.btkservice,'org.yatbz.dbusbtkeyboardgpioservice')

	def send_key_dbus(self):
		bin_str=""
		element=self.state[2]
		for bit in element:
			bin_str += str(bit)
		self.iface.send_keys(int(bin_str,2),self.state[4:10])

	def transmit_key_down(self, key_id):
		self.state[4]=key_id
		self.send_key_dbus()
		print "Key Down"

	def transmit_key_up(self):
		self.state[4]=0
		self.send_key_dbus()
		print "Key Up"

	def event_loop(self):
		released = True
		while True:
			for i in range(0, len(self.GPIOs),1):
				if (GPIO.input(self.GPIOs[i]) == GPIO.HIGH and released):
					self.transmit_key_down(self.connectedKeys[i])
					time.sleep(self.REPEAT_KEY_DELAY)
					released = False
				elif (GPIO.input(self.GPIOs[i]) == GPIO.LOW and not(released)):
					self.transmit_key_up()
					time.sleep(self.REPEAT_KEY_DELAY)
					released = True

if __name__ == "__main__":

	print "Settings up GPIO Bluetooth Keyboard emulator client"

	dc = GPIOClient()

	print "starting event loop"
	dc.event_loop()
