""" EE 250L Lab 02: GrovePi Sensors

List team members here.
Camille Gutierrez

Insert Github repository link here.
https://github.com/usc-ee250-spring2021/lab02-camillegutierrez.git

Video Demo link:
https://drive.google.com/file/d/1I3--eXUVcygtp0ZJ51uTKNxibtVY85oV/view?usp=sharing

"""

"""python3 interpreters in Ubuntu (and other linux distros) will look in a 
default set of directories for modules when a program tries to `import` one. 
Examples of some default directories are (but not limited to):
  /usr/lib/python3.5
  /usr/local/lib/python3.5/dist-packages

The `sys` module, however, is a builtin that is written in and compiled in C for
performance. Because of this, you will not find this in the default directories.
"""
import sys
import time
# By appending the folder of all the GrovePi libraries to the system path here,
# we are successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi
from grove_rgb_lcd import *
from grovepi import *

"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 grovepi_sensors.py` in terminSal, this if-statement will 
be true"""
if __name__ == '__main__':
	PORT = 4  #D4

	ultrasonic_ranger = 3 #Grove Ultrasonic ranger connected to digital port D3
	potentiometer = 1 #Grove rotary angle sensor connected to analog port A1

	grovepi.pinMode(potentiometer,"INPUT")
	grovepi.pinMode(ultrasonic_ranger, "INPUT")
	time.sleep(1)

	# Reference voltage of ADC is 5v
	adc_ref = 5

	# Vcc of the grove interface is normally 5v
	grove_vcc = 5

	# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
	full_angle = 300


	while True:

		try:
			# Read sensor value from potentiometer
			sensor_value = grovepi.analogRead(potentiometer)

			# Calculate voltage
			voltage = round((float)(sensor_value) * adc_ref / 1023, 2)

			# Calculate rotation in degrees (0 to 300)
			degrees = round((voltage * full_angle) / grove_vcc, 2)

			threshhold = int(round((degrees/full_angle) * 1023)) 

			distant = ultrasonicRead(ultrasonic_ranger)
			
			line2 = str(distant) + 'cm'

			if distant <= threshhold:
				line1 = str(threshhold) + 'cm OBJ PRES \n'
			else:
				line1 = str(threshhold) + 'cm          \n'

			setText_norefresh(line1 + line2)

			#So we do not poll the sensors too quickly which may introduce noise,
			#sleep for a reasonable time of 200ms between each iteration.
			time.sleep(0.2)

			print(grovepi.ultrasonicRead(PORT))
		
		except Exception as e:
			print (e)
