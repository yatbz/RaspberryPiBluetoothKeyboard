This is a program which allows you to send bluetooth entries live using bluetooth to a receiving device like PC or iPad.
It is also possible to send defined key presses triggered by GPIO Pins. Another possible method is to send prepared strings.
There for there are three different starting files:
Keyboard_Start.py is for sending live Keyboard enties.
GPIO_Start.py is for sending Keys triggered by GPIO.
SendString_Start.py is responsible for sending a string.

Keyboard_Start.py:

For running this script an USB Keyboard should be connected. 
The Raspberry will only be available on bluetooth if a keyboard is connected.

GPIO_Start.py

For using this script first GPIO pins and keys have to be defined.
Therefor enter der folder Subprograms and open GPIO_Key.py .
Inside the GPIOClient class you will find an a list called GPIOs.
Each entry (seperated by ,) represents a GPIO pin.
Beneath is a list that is called connectedKeys.
If you want GPIO 26 to trigger KEY_PAGEDOWN the keyid for pagedown has to be in 
the same index as the GPIO pin but in the connectedKeys list.
You can find the keyid inside the same folder: keymap.py.
The lists can be extendet or shortend.
REPEAT_KEY_DELAY defines the minimum time between each state change at the GPIOs. It is in seconds.
This configuration is for building a foot controller for scrolling through documents.
Here GPIOs are triggered if the voltage raises (maximum +3.3V).

SendString_Start.py

If you want to send a string you only have to run this script with
python SendString_Start.py
and add a string behind:
python SendString_Start.py "My String"
Only one String can be send. 
The receiving device is receiving each letter with a specified delay. This delay can be changed in Subprograms/send_string.py at KEY_DELAY. It is again in seconds.

All scripts can be run in the background. And using crontab:
For crontab after reboot you have to enter the following command:

@reboot sleep 3; screen -d -m -S "A name of your choice" bash -c "sudo python path/to/the/script"

For changing the showen bluetooth name you have to edit Subprograms/main.conf Name


For reseting the system the following commands have to be run:

sudo pkill screen

sudo pkill python

sudo /etc/init.d/bluetooth start

sudo rm /etc/dbus-1/system.d/org.yatbz.dbusbtkeyboardgpioservice.conf

Edit /etc/bluetooth/main.conf and add # in front of 

Name

Class

Pairable Timeout

Discoverable Timeout



This project is based on the work of:
http://yetanotherpointlesstechblog.blogspot.com/
