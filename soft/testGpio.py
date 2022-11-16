#!/usr/bin/env python
# -*- coding: utf-8 -*-


#GPIO 17 on/off motor
onOff=17
#GPIO 27 increase speed
incSp=27
#GPIO 22 decrease speed
decSp=22

import RPi.GPIO as GPIO

import time


def initGpio(channel):
	
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(channel,GPIO.IN)
	GPIO.setup(channel,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	
def callBackOn(self):
		
	
	if (GPIO.input(onOff)==0):
		
		print "START MOTOR"
		
	else:

		print "STOP MOTOR"
		
def callBackPlus(self):
	
	if (GPIO.input(incSp)==0):
		print "test1"
		print "SPEED++"
		
def callBackMinus(self):

	if (GPIO.input(decSp)==0):
		print "test2"
		print "SPEED--"
	
if __name__ == "__main__":
	
	initGpio(onOff)
	initGpio(incSp)
	initGpio(decSp)
	GPIO.add_event_detect(onOff,GPIO.BOTH,callback=callBackOn)
	#GPIO.add_event_detect(incSp,GPIO.FALLING,callback=callBackPlus,bouncetime=100)
	#GPIO.add_event_detect(decSp,GPIO.FALLING,callback=callBackMinus,bouncetime=100)
	
	while True:
		
		"test"
