This project is to make a Raspberry pi into an OBS tallylight.
This is tested on a pi V1 with a wireless USB module for a wireless connection.
see https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

For other pi models use other pin numbers and change tally.py
The red led and green led are connected with a 330ohm resistor.
see https://gpiozero.readthedocs.io/en/stable/

Install on the pi:
- gpiozero
	sudo apt-get install python-gpiozero
	(sudo apt-get install python3-gpiozero)
- nginx and php
	see https://www.raspberrypi.org/documentation/remote-access/web-server/nginx.md
- php-xml
	sudo apt-get install php-xml

install in /home/pi/
	tally.py
	tally.xml
install in /var/www/html/
	index.php
	gpio.php (for testing led)

set rights in /var/www/
	sudo chown -R pi:www-data /var/www
	sudo chmod u+rwx,g+srw-x,o-rwx /var/www/
	sudo chmod u+rw,g+r-xw,o-rwx /var/www/html/index.php
set rights in /home/pi/
	sudo chmod u+rw,g+rw-x,o-rwx /home/pi/tally.xml

To make the python script start at boot:
	see https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/
	sudo nano /etc/rc.local
	just above line 'exit 0' insert:
	sudo python /home/pi/tally.py &
	don't forget the & at the end for running it as a daemon
	
after starting the pi with the script running in background goto:
(I use ipscan24 to find the pi on the network.)
http://<pi IP address>/gpio.php for testing the led.
http://<pi IP address>/index.php for configuring the 'tally'
After configuring the 'tally' reboot the pi.

Next project steps:
- Raspberry pi 3B+
- 10mm RGB led's on hot/cold shoe, wire connected to pi
	red = programm
	green = preview
	blue = not connected to OBS.
- film to show it working.
- publish a complete configured image for Raspberry pi 3B+

It would be nice when the pi also can be used as a intercom system with a USB headset.