#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import Qt, QtCore, QtGui
import PyQt4.Qwt5 as qwt
from PyQt4.Qwt5 import QwtPlotCurve
#from qwt_plot_curve import QwtPlotCurve

/**
 * @file Visco5.py
 * 
 *
 * @mainpage Grapical User Interface For portable viscometer
 * 
 *
 * @section intro_sec Introduction
 *
 * To visualize the data, we developed software in Python that is implemented in the Raspberry PI 3 
 * running under Linux. The PyQt module creates a graphical interface integrating graphs, command buttons,
 * and a toolbar to interact with the viscometer. When starting the software, the program checks 
 * whether the on switch is set to 0 and then launches the initialization sequence and 
 * searches for the names of the serial ports to which the motor board and 
 * the temperature sensor RF receiver module are connected. 
 * When these steps are valid, the user can execute the acquisition and data plotting.
 *
 *
 * @section author Author
 *  Visco5.pywritten by Thierry Latchimy OPGC CNRS
 * 
 *
 * @section license License
 *
 * BSD license, all text here must be included in any redistribution.
 * See the LICENSE file for details.
 *
 */



from view10 import Ui_MainWindow # created with QtDesigner and pyuic
from dialog import Ui_Dialog as Step_Ui_Dialog
from dialogSpeed import Ui_Dialog as Speed_Ui_Dialog
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from thermocouples_reference import thermocouples
import sys
import os
import time
import random
import serial
import glob
import datetime
import numpy
import math
import locale
import os.path
from subprocess import Popen, PIPE
import RPi.GPIO as GPIO
import unicodedata 
import bitstring

#Set true if need linearization of Torque
linear=False

# Linear curve 1 (Vadc-7.507)/313.6 for Vadc<60 mV
# Linear curve 2 (Vadc + 6.137)/299.13 for Vadc>=60 mV
VadcTrh=60


#GPIO 17 on/off motor
onOff=17
#GPIO 27 increase speed
incSp=27
#GPIO 22 decrease speed
decSp=22

baudMotor=115200
baudSer=57600
ser=serial.Serial()
ser2=serial.Serial()


typek=thermocouples['K']
degC=unicodedata.lookup('DEGREE SIGN')+"C"
speedLim=30
speedStart=0.5
dataFolder="/media/pi/DATAVISCO/"
scriptFolder="script_speed"
###Torque sensor parameters###
#sensitivity mV/V
Se = 2.0
#Amplifier gain
G  = 300.0
#Sensor dc power supply /V
Vpws = 5.0
#Max torque 2.5N.M
Tmax = 2.50
#Full scalle output sensor /V

Vpe = ((Se * Vpws)*G)/1000
Vpe2 = Se*Vpws

#Sensitivity after amplifier : Kt N.m/V

Kt = Tmax/Vpe

#JoySpeedRpm = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.5,2,2.5,3,4,5,6,7,8,9,10,11,\
#		12,13,14,15,16,17,18,19,20,21,22,25,26,27,28]

#ADC offset voltage(mV)
Voffset =0
class MyForm(QtGui.QMainWindow,Ui_MainWindow):

	def __init__(self,parent=None):
		super(MyForm, self).__init__(parent)
		self.setupUi(self)
		#init all functions
		self.JoySpeedRpm = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.5,2,2.5,3,4,5,6,7,8,9,10,11,\
		12,13,14,15,16,17,18,19,20,21,22,25,26,27,28]
		
		#Create list of speed if gear = 1/25
		# 1,2,3,4,5,6,7,8,9,10,15,20,25,30,35, after every 5 until 100
		
		var_deb=10
		i = 0
		self.JoySpeedRpm2 = []
		
		while(var_deb<101) :
	
			if(i<9):
				self.JoySpeedRpm2.append(i+1) 
			else :
				self.JoySpeedRpm2.append(var_deb)
				var_deb+=5
			i+=1
		self.tempXbee=0.0
		self.realTimeData=0.0
		self.listPlot=[self.qwtPlotdata,self.qwtviewPlot]
		self.init_plots()
		self.initZoomer(self.listPlot)
		self.init_viewer()
		self.init_timer()
		self.flagNotemp=False
		self.listComPort=self.list_serial_port()
		self.init_Combox(self.listComPort)
		self.SpeedDiv=self.getGear()
		print"**Checking communication with RF Transmitter and Motor**"
		self.portComXbee=self.testCom(self.listComPort,2)
		self.listComPort=self.list_serial_port()
		self.portCom2=self.testCom(self.listComPort,1)
		time.sleep(5)
		self.comRs232(self.portCom2,baudMotor)
		self.initPicker()
		self.setIndexCom(self.portCom2)
		self.Tacquisition=0.1
		self.statusBar()
		#self.Ttrh=self.TorqueTreshTimedoubleSpinBox.value()
		self.Ttrh=2500
		#create global variable
		#Joystick speed value

		self.speedCell=[]     #data from table
		self.dwellTimeCell=[]
		self.tsamplePic=0.100 #Tsample =0.100 s
		self.speedData=[] # data from file
		self.dwellData=[]
		self.oldTime=0
		self.nbSample=0
		self.SpeedDiv=100 #Nout=Nin/100
		self.convRpm=(60.0/(2*(math.pi)))
		self.convRad=1/self.convRpm
		self.Vref=3.30
		self.quantum10bits=(self.Vref/1024.0)
		self.Nbstep=0
		self.i=0
		self.tInit=0
		self.tabSp=[]
		self.tabTq=[]
		self.tabTemp=[]
		self.avgInc=0
		self.tabJoySpeed=[]
		self.manBut=True
		
		#Create value of joystick speed
		
		for i in range(len(self.JoySpeedRpm)):
			
			self.tabJoySpeed.append(self.JoySpeedRpm[i]*self.convRad*self.SpeedDiv)
		
		#style sheet
		
		self.toolBar.setStyleSheet("QToolButton#actionSTOP_MOTOR { background:red }")

		
		#Nech : sample numbers averaging before printing
		self.Nech=40
		self.update=True
		self.closeAcq=False
		self.flagUpdate=True
		self.flagStop=True
		self.flagdataStep=False
		self.flagStep=False
		self.flagSpeedX2=False
		self.flagSpeediv2=False
		

		#init index of tabjoySpeed
		self.indexSpeed=4
		
		self.statusBar()
		self.zoom(False)
		self.showInfo()

		##create object for windows dialog
		self.stepMode=stepDialog(self)
		self.speedDia=speedDialog(self)
		self.speedDia.SpeedControl.setValue(speedStart)
		self.speedDia.SpeedControl.lineEdit().deselect()
		#######################

		#slot signal
		########################
		self.actionSTOP_MOTOR.setCheckable(True)
		self.actionSPEED_FIX.setCheckable(True)
		self.actionSPEED_STEP.setCheckable(True)
		self.actionSave_File.setCheckable(True)
		self.actionZOOM.setCheckable(True)
		self.actionSTART_ACQ.triggered.connect(self.start_Acq)
		self.actionSTOP_MOTOR.triggered.connect(self.onOffMotor)
		self.actionSTOP_Plot.triggered.connect(self.closeAcquire)
		self.actionSPEED_FIX.triggered.connect(self.SpeedCde)
		self.actionSPEED_STEP.triggered.connect(self.stateButtonStep)
		self.actionINIT_MOTOR.triggered.connect(self.init_Motor)
		self.radioButtonTemperature.toggled.connect(self.clearPicker)
		self.radioButtonTorque.toggled.connect(self.clearPicker)
		self.radioButtonSpeed.toggled.connect(self.clearPicker)
		self.pushButtonLoadData.clicked.connect(self.loadData)
		self.checkBoxSpeed.toggled.connect(self.update_View)
		self.checkBoxTorque.toggled.connect(self.update_View)
		self.checkBoxTempC.toggled.connect(self.update_View)
		self.actionZOOM.toggled.connect(self.zoom)
		self.actionRAZ_PLOT.triggered.connect(self.raz_curve)
		self.speedDia.toolButtonPlus.clicked.connect(self.arrowPlus)
		self.speedDia.toolButtonMinus.clicked.connect(self.arrowMinus)
		#Create a table with default value
		self.update_Table()
		
		#slot signal
		self.speedDia.SpeedControl.valueChanged.connect(self.onOffMotor)
		self.stepMode.pushButtonSavefile.clicked.connect(self.save_Script_File)
		self.stepMode.pushButtonOpenfile.clicked.connect(self.open_file)
		self.stepMode.pushButtonOK.clicked.connect(self.setIconRun)
		
		self.stepMode.SpinBoxStep.valueChanged.connect(self.update_Table)
		self.stepMode.tableWidgetStep.setHorizontalHeaderLabels(['Speed(rpm)','Dwell time(s)'])
		self.actionSave_File.triggered.connect(self.save_Data_File)
		self.toolButtonUpdateCom.clicked.connect(self.update_com)
		self.connect(self.picker,QtCore.SIGNAL('moved(const QPoint &)'),self.moved)
		self.connect(self.picker,QtCore.SIGNAL('selected(const QPolygon &)'),self.selected)
		self.connect(self.picker2,QtCore.SIGNAL('moved(const QPoint &)'),self.moved)
		self.connect(self.picker2,QtCore.SIGNAL('selected(const QPolygon &)'),self.selected)
		self.connect(self.picker3,QtCore.SIGNAL('moved(const QPoint &)'),self.moved)
		self.connect(self.picker3,QtCore.SIGNAL('selected(const QPolygon &)'),self.selected)
		#load data of table and close  the dialog
		self.stepMode.pushButtonOK.clicked.connect(self.load_Cell)
		self.actionQUIT_ALL.triggered.connect(self.closeAll)
		#Icon for on/off motor
		self.iconRun=QtGui.QIcon()
		self.iconRun.addPixmap(QtGui.QPixmap("playMotor.png"))
		self.iconStop=QtGui.QIcon()
		self.iconStop.addPixmap(QtGui.QPixmap("delete.png"))
		self.actionSTOP_MOTOR.setIcon(self.iconRun)
		
		#Icon for speed step motor
		self.iconStepRun=QtGui.QIcon()
		self.iconStepRun.addPixmap(QtGui.QPixmap("steprun.jpg"))
		self.iconStepStop=QtGui.QIcon()
		self.iconStepStop.addPixmap(QtGui.QPixmap("step.png"))
		self.actionSPEED_STEP.setIcon(self.iconStepStop)
		
		#Icon for savefile 
		self.iconSaveRun=QtGui.QIcon()
		self.iconSaveRun.addPixmap(QtGui.QPixmap("record.png"))
		self.iconSaveStop=QtGui.QIcon()
		self.iconSaveStop.addPixmap(QtGui.QPixmap("save.png"))
		self.actionSave_File.setIcon(self.iconSaveStop)
		
		
		#gear ratio
		self.comboBoxGear.currentIndexChanged.connect(self.getGear)
		
	def stateOfStart(self):
		#test if button start is on
		print "**Check state of start button**"
		time.sleep(3)
		if(GPIO.input(onOff)==0):
			self.showMsgBtn()
			exit()
		else:
			print "Button:OK!!"
			print "Ready"
			time.sleep(3)
		

	def setIconRun(self):
		print"******SETICON Run*********"
		self.actionSPEED_STEP.setIcon(self.iconStepRun)
		
	def setIconSave(self):
		print"******SETICON Save*********"
		self.actionSave_File.setIcon(self.iconSaveRun)
	def getGear(self):
		
		if (self.comboBoxGear.currentIndex() ==0):
			
			self.SpeedDiv = 100
			self.JoySpeedRpm = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.5,2,2.5,3,4,5,6,7,8,9,10,11,\
		12,13,14,15,16,17,18,19,20,21,22,25,26,27,28]
		else:
			
			self.SpeedDiv = 25
			self.JoySpeedRpm = Self.JoySpeedRpm2
		print "**GEAR RATIO**:",self.SpeedDiv
	
	def speedPlus(self):
		print "speed++"
		self.flagSpeedX2=True

	def speedMinus (self):
		print "speed--"
		self.flagSpeediv2=True
		
	def arrowPlus (self):
		self.speedDia.SpeedControl.stepBy(1)
		
	def arrowMinus (self):
		self.speedDia.SpeedControl.stepBy(-1)
		
		
	
	def onOffMotor(self):
		if((self.manBut==False)and (GPIO.input(onOff)==0)):
			
			#print message if manual start button is on
			self.showMsgBtn()
			return

		if (self.actionSTOP_MOTOR.isChecked()):
			print"*****Button ON****"
			self.flagStop=True
			self.actionSTOP_MOTOR.setIcon(self.iconStop)
			self.update_Speed()
			
		else:
			print"*****Button OFF****"
			#init icon 
			self.actionSTOP_MOTOR.setIcon(self.iconRun)
			self.actionSPEED_STEP.setCheckable(False)
			self.actionSPEED_STEP.setCheckable(True)
			self.actionSPEED_STEP.setIcon(self.iconStepStop)
			#init index of step array
			self.i=-1
			self.dataSpeedStep=0
			#init index of joySpeed
			self.indexSpeed=-1
			self.stop_Motor()
			
	def load_Cell(self):
		i=0
		j=0
		self.speedCell=[]
		self.dwellTimeCell=[]
		#get numbers of row tqwidget table
		Nbrow=self.stepMode.tableWidgetStep.rowCount()
		#Nbrow=self.stepMode.SpinBoxStep.value()
		Nbcol=2
		for j in range(Nbcol):
			
			for i in range(Nbrow):
				data=self.stepMode.tableWidgetStep.item(i,j).text()
				if (j==0):
					self.speedCell.append(float(data))
				else:
					self.dwellTimeCell.append(float(data))
			i=0
		print "Speed:"
		print self.speedCell
		print "Dwell Time:"
		print self.dwellTimeCell
		
		#close window dialog
		self.stepMode.close()


	def update_Table(self):
		self.row=self.stepMode.SpinBoxStep.value()
		self.stepMode.tableWidgetStep.setRowCount(self.row)

	def stateButtonStep(self):
			self.stepMode.show()
			self.flagStep=True
			
	def SpeedCde(self):
		if (self.flagStep==True):
			self.flagStep=False
			self.flagdataStep=False
		self.speedDia.show()


	def init_viewer(self):
		title=['Data viewer','Torque','Temperature','Speed']
		self.qwtviewPlot, self.curveViewTq,self.curveViewTp,self.curveViewSp=self.init_curve(self.qwtviewPlot, title,\
				xmin=0, xmax=120000, ymin=0, ymax=2.5,flag=True,idView=1)
		self.x=[]
		self.y=[]
		self.y1=[]
		self.y2=[]
		
		# legend
		legendView=qwt.QwtLegend()
		self.qwtviewPlot.insertLegend(legendView, qwt.QwtPlot.TopLegend)
		pass

	def init_plots(self):
		title=['Real Time Data','Torque','Temperature']
		self.qwtPlotdata, self.curveTq,self.curveTp=self.init_curve(self.qwtPlotdata, title,\
				xmin=0, xmax=120000, ymin=0, ymax=2.5,flag=False,idView=0)
		self.qwtPlotDataZoom, self.curveTqZoom,self.curveTpZoom=self.init_curve(self.qwtPlotDataZoom, title,\
				xmin=0, xmax=120000, ymin=0, ymax=2.5,flag=True,idView=0)
		self.x=[]
		self.y=[]
		self.y1=[]
		pass

	def init_timer(self):
		self.timer = QtCore.QTimer()
		QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"),self.update_data)
		
		

	def init_curve(self, plot, title, xmin=0, xmax=100,ymin=0, ymax=100,flag=True,idView=0):
		
		plot.xmin = xmin
		plot.xmax = xmax
		plot.ymin = ymin
		plot.ymax = ymax
		
		if (flag==True):
			plot.setAxisTitle(qwt.QwtPlot.xBottom, self.tiny_title("Time(s) "))
		#Autoscale xAxis
		plot.setAxisAutoScale(qwt.QwtPlot.xTop)
		plot.setAxisAutoScale(qwt.QwtPlot.xBottom)
		
		# Autoscale First axis
		plot.setAxisTitle(qwt.QwtPlot.yLeft, self.tiny_title("Torque(mN.m)"))
		plot.setAxisAutoScale(qwt.QwtPlot.yLeft)
			
		
		#Autoscale Second axis
		plot.enableAxis(qwt.QwtPlot.yRight)
		plot.setAxisTitle(qwt.QwtPlot.yRight, self.tiny_title("Temperature("+degC+")"))
		plot.setAxisAutoScale(qwt.QwtPlot.yRight)
		
		#Set background color and grid
		plot.setCanvasBackground(Qt.QColor(Qt.Qt.black))
		grid = qwt.QwtPlotGrid()
		grid.setPen(Qt.QPen(Qt.Qt.white, 0, Qt.Qt.DashLine))
		grid.attach(plot)
		
		# legend
		legend=qwt.QwtLegend()
		self.qwtPlotdata.insertLegend(legend, qwt.QwtPlot.TopLegend)

		#Torque curve
		if (idView==0):
			
			#Temperature curve	
			self.curve2  = QwtPlotCurve(title[2])
			self.curve2.attach(plot)
			self.curve2.setPen(Qt.QPen(Qt.Qt.blue, 1.5))
			self.curve2.setYAxis(qwt.QwtPlot.yRight)
			
			self.curve1 = QwtPlotCurve(title[1])	
			self.curve1.attach(plot)
			self.curve1.setPen(Qt.QPen(Qt.Qt.green, 1.5))
			self.curve1.setYAxis(qwt.QwtPlot.yLeft)
			self.curve1.setData([0], [0])
			
			
			
			
		else:
			
			#Temperature curve	viewer
			self.curViewTp  = QwtPlotCurve(title[2])
			self.curViewTp.attach(plot)
			self.curViewTp.setPen(Qt.QPen(Qt.Qt.blue, 1.5))
			self.curViewTp.setYAxis(qwt.QwtPlot.yRight)
			
			#Speed curve viewer
			self.curViewSp  = QwtPlotCurve(title[3])
			self.curViewSp.attach(plot)
			self.curViewSp.setPen(Qt.QPen(Qt.Qt.red, 1.5))
			self.curViewSp.setYAxis(qwt.QwtPlot.yRight)
		
			#Torque curve viewer
			self.curViewTq = QwtPlotCurve(title[1])	
			self.curViewTq.attach(plot)
			self.curViewTq.setPen(Qt.QPen(Qt.Qt.green, 1.5))
			self.curViewTq.setYAxis(qwt.QwtPlot.yLeft)
			self.curViewTq.setData([0], [0])
		
		plot.replot()
		
		if (idView==0):
			return plot, self.curve1,self.curve2
		else:
			return plot, self.curViewTq,self.curViewTp ,self.curViewSp
			
	def update_Speed(self):
		self.update=False
		if self.flagdataStep==False:
			if(self.flagSpeedX2==True):
				self.Speed=self.speedM
				self.speedDia.SpeedControl.setValue(self.speedM/(self.convRad*self.SpeedDiv))
					
			elif(self.flagSpeediv2==True):
				self.Speed=self.speedM
				self.speedDia.SpeedControl.setValue(self.speedM/(self.convRad*self.SpeedDiv))
				
			else:
				if(self.actionSPEED_FIX.isChecked()):
					print "Send speed command"
					self.Speed=self.speedDia.SpeedControl.value()*self.convRad*self.SpeedDiv #speed in rad/s
				else:
					#start at speed min
					self.Speed=speedStart*self.convRad*self.SpeedDiv #speed in rad/s
		else:
			
			self.Speed=self.dataSpeedStep*self.convRad*self.SpeedDiv #speed in rad/s
			print "***STEP MODE***",self.dataSpeedStep
		
		#Mark
		Mark =255
		#start of data
		Id=0
		#Cmd=1 speed regulation
		Cmd=1
		SpeedmH=0
		SpeedmL=0
		TqH=0
		TqL=0
		d4H = 0
		d4L=0
		speedH,speedL=self.floatTo2byte(self.Speed,1)
		DataFrameSpeed=[Mark,Id,Cmd,speedH,speedL,SpeedmH,SpeedmL,TqH,TqL,d4H,d4L]
		ck=self.checkSum(DataFrameSpeed)
		DataFrameSpeed.append(ck)
		trameSpeed=self.trameCommand(DataFrameSpeed)
		self.print_trame(trameSpeed)
		cmd=trameSpeed.decode("hex")
		self.writeRS(ser,cmd)
		self.writeRS(ser,cmd)
		time.sleep(0.1)
		ser.flushInput #flush input buffer, discarding all its contents
		ser.flushOutput#flush output buffer, aborting current output
				 #and discard all that is in buffer
		self.update=True


	def update_data(self):

		if ((ser.inWaiting())and (self.update==True)):
		
			dataFrame =ser.readlines(12)
			frameDec=self.trameProcess(dataFrame)
			print "size of frame :",len(frameDec)
			if(len(frameDec)==12):
				
				SpeedLow= frameDec[4]
				SpeedHigh= frameDec[3]
				SpeedLowMeas= frameDec[6]
				SpeedHighMeas= frameDec[5]
				TorqueHigh=frameDec[7]
				TorqueLow=frameDec[8]
				#print "***Frame***:",frameDec
				self.speed=self.byteTofloat(SpeedHigh,SpeedLow,1)
				self.speedM=self.byteTofloat(SpeedHighMeas,SpeedLowMeas,1)

				if (self.speedM<0):
					self.speedM=0
				self.dataFloat=self.byteTofloat(TorqueHigh,TorqueLow,2)
				if(linear==True):
					if(self.dataFloat*1000<VadcTrh):
						self.torque=((Tmax*1000)/Vpe2)*(((self.dataFloat*1000)-7.507)/313.6)
					else:
						self.torque=((Tmax*1000)/Vpe2)*(((self.dataFloat*1000)+6.137)/299.13)
				
				else:
					self.torque=(self.dataFloat*1000 -Voffset)*Kt
				
				if(self.torque>2600):
					
					self.torque=0
					
				
				#self.torque=(self.dataFloat*1000 -Voffset)
				#flagNotemp= true if no temperature sensor
				if (self.flagNotemp==True):
					
					frameXbee=[0]
					
				else:
					print "Start Xbee"
					print self.portComXbee
					with serial.Serial(port=self.portComXbee, baudrate=57600 ) as portComXbee:
						frameXbee=portComXbee.readline()
					print "Data OK"
					
				
				#print "Speed feedback(rpm):",
				#print (self.speed*self.convRpm)/self.SpeedDiv,
				#print "Speed Measure(rpm):",
				#print (self.speedM*self.convRpm)/self.SpeedDiv,
				#print "Float value Torque:",self.dataFloat
				#print "Torque(mN.m) :",
				#print self.torque
				#print "Temperature(degC):",
				#print frameXbee[1:]
				self.speed=round((self.speedM*self.convRpm)/self.SpeedDiv,2)
				print "****INDEX*****:",self.indexSpeed
				print "****SPEED*****:",round((self.tabJoySpeed[self.indexSpeed]*self.convRpm)/self.SpeedDiv,2)
				#print "****Length Tab*****:",len(self.tabJoySpeed)
				
				if (len (frameXbee)>2):
					
					data1=frameXbee.split('\r\n')
					#data1=['$val1,val2','\r\n')
					#val1=Thermocoupler value on 24bits
					#val2=Internal temperature of ADC on 24 bits
					
					data2=data1[0]
					#data2=['$val1,val2']
					
					if (data2[0]=="$"):
						data2=(data2[1:]).split(',')
						try:
							tc2=float(data2[0])
						except:
							tc2=0
						
						try:
							temp=data2[1]
							
						except:
							temp='0'
							
						s = bitstring.pack('int:24',float(temp))
	
						c = s[:14]
						t = c.int*0.03125
		
						adcvoltage =(tc2/(2**23))*(2.048/4)
						self.Tkval= typek.inverse_CmV(adcvoltage*1000,Tref=t)


				#calulate average value for 10 samples
				if (self.avgInc<self.Nech):
					
					self.tabSp.append(self.speed)
					self.tabTq.append(self.torque)
					if (self.flagNotemp==True):
						self.tabTemp.append(0)
						self.Tkval=0
					else:
						
						self.tabTemp.append(self.Tkval)
				else:
					
					avgTorque=sum(self.tabSp)/len(self.tabSp)
					avgTq=sum(self.tabTq)/len(self.tabTq)
					avgTemp=sum(self.tabTemp)/len(self.tabTemp)
					self.tabSp=[]
					self.tabTq=[]
					self.tabTemp=[]
					self.avgInc=0
					
					self.lineEditTorque.setText(str(round(self.torque,3)))
					self.lineEditSpeed.setText(str(self.speed))
					self.lineEditTemperature.setText(str(round(self.Tkval,2)))
					
				self.avgInc+=1
				
				if(self.torque>self.Ttrh):
					print"OVERLOAD"
					self.speedDivBy2=self.speedM/2.0
					print "Speed:",self.speedDivBy2
					self.div_Speed(self.speedDivBy2)
				
				if(self.flagSpeedX2==True):
					
					#self.speedMultBy2=self.speedM*1.5
					self.speedMultBy2=self.tabJoySpeed[self.indexSpeed]
					#max speed : 28 tr/min
					#speed in rad/s
					if(self.speedMultBy2<speedLim*self.convRad*self.SpeedDiv): 
						self.speedM=self.speedMultBy2
						self.update_Speed()
						self.flagSpeedX2=False
					else:
						self.speedM=self.speedMultBy2/2.0
						self.update_Speed()
						self.flagSpeedX2=False
					
				if(self.flagSpeediv2==True):
					self.speedDiv2=self.tabJoySpeed[self.indexSpeed]
					#self.speedDiv2=self.speedM/1.5
					self.speedM=self.speedDiv2
					self.update_Speed()
					self.flagSpeediv2=False
				
				currentTimeMs=int(round(time.time() * 1000))
				timeData=currentTimeMs-self.oldTime
				
				
				#print "****DELTA TIME****  : " + str(timeData)
				#print "**REAL TIME VALUE ****  : " + str(realTimeData)
				if (self.nbSample==0):
					self.x.append(0)
					self.curDwellt=0
				else:
					#self.curDwellt=self.tsamplePic*self.nbSample
					self.realTimeData+=(timeData/1000.0)
					self.curDwellt=self.realTimeData
					#print self.curDwellt
					self.x.append(self.curDwellt)
				
				self.curSpeed=(self.speedM*self.convRpm)/self.SpeedDiv
				self.curTorque=self.torque
				self.curTempC=self.Tkval
				self.y.append(self.curTorque)
				self.y1.append(self.curTempC)
				self.oldTime=currentTimeMs
				self.nbSample+=1
				
				if (float(self.curDwellt)>(self.WindowTimedoubleSpinBox.value())):
					
					NbLastPts=int((self.WindowTimedoubleSpinBox.value())/self.tsamplePic)
					self.xz=self.x[len(self.x)-NbLastPts:]
					self.yz=self.y[len(self.y)-NbLastPts:]
					self.yz1=self.y1[len(self.y1)-NbLastPts:]
					
				else:
					
					self.xz=self.x
					self.yz=self.y
					self.yz1=self.y1


				self.update_curve(self.qwtPlotdata,self.curveTq,self.x,self.y)
				self.update_curve(self.qwtPlotdata,self.curveTp,self.x,self.y1)
				
				# second plotting , plot cuve for the last x seconds data
				self.update_curve(self.qwtPlotDataZoom,self.curveTqZoom,self.xz,self.yz)
				self.update_curve(self.qwtPlotDataZoom,self.curveTpZoom,self.xz,self.yz1)
				self.zoomers[0].setZoomBase(False)
				self.zoomers[1].setZoomBase(False)
				self.zoomers[2].setZoomBase(False)
				self.zoomers[3].setZoomBase(False)
			
				#print self.curDwellt
				
				#write to file
				temp=[]
				temp=datetime.datetime.today().strftime("%d/%m/%y-%H:%M:%S.%f")
				self.curDate=temp[:len(temp)-3]
				#print "date :"+self.curDate
				try:
					self.write_dataToFile(self.filename_Data,self.curDate,self.curDwellt,self.curSpeed,self.curTorque,self.curTempC)
				except:
					pass
				
				if(self.flagStep and self.flagStop and self.actionSTOP_MOTOR.isChecked() ):
					self.actionSPEED_STEP.setIcon(self.iconStepRun)
					self.Nbstep=len(self.speedCell)
					print "data step", self.Nbstep
					self.dataSpeedStep=float(self.speedCell[self.i])
					print "dataSpeed", self.dataSpeedStep
					self.flagdataStep=True
					if (self.flagUpdate):
						self.tInit=self.curDwellt
						self.update_Speed()
						print"curtime:"+str(self.curDwellt)
						print"Valsup:"+str((self.dwellTimeCell[self.i]+self.tInit))
					if (float(self.curDwellt)>=float(self.dwellTimeCell[self.i]+self.tInit)):
						flagUpdate=True
						self.tInit=self.curDwellt
						if self.i==(self.Nbstep-1):
							self.flagStop=False
							self.flagdataStep=False
							self.flagStep=False
							self.i=0
							self.actionSTOP_MOTOR.setIcon(self.iconRun)
							self.actionSTOP_MOTOR.setCheckable(False)
							self.actionSTOP_MOTOR.setCheckable(True)
							self.actionSPEED_STEP.setCheckable(False)
							self.actionSPEED_STEP.setCheckable(True)
							self.actionSPEED_STEP.setIcon(self.iconStepStop)

							#End of step speed then stop motor
							self.stop_Motor()
							
							
						else :
							self.i+=1
							self.flagUpdate=True
							
								
								
					else:
						self.flagUpdate=False
				
	#reset all graph		
	def raz_curve(self):
		self.closeAcquire()
		#self.__init__
		
		self.nbSample=0
		self.x=[]
		self.y=[]
		self.y1=[]
		self.xz=[]
		self.yz=[]
		self.yz1=[]

		if (self.tabWidgetIHM.currentIndex() == 0):
			print "RAZ GRAPH"
			self.update_curve(self.qwtPlotdata,self.curveTq,self.x,self.y)
			self.update_curve(self.qwtPlotdata,self.curveTp,self.x,self.y1)

			self.update_curve(self.qwtPlotDataZoom,self.curveTqZoom,self.xz,self.yz)
			self.update_curve(self.qwtPlotDataZoom,self.curveTpZoom,self.xz,self.yz1)
			#reset speed control value
			
			self.speedDia.SpeedControl.setValue(speedStart)
	
		elif  (self.tabWidgetIHM.currentIndex() == 1):
			print "RAZ GRAPH"
			self.update_curve(self.qwtviewPlot,self.curveViewTq,self.x,self.y)
			self.update_curve(self.qwtviewPlot,self.curveViewTp,self.x,self.y1)
			self.update_curve(self.qwtviewPlot,self.curveViewSp,self.x,self.y2)
				
		else:
		
			pass
			
		
			
	def update_curve(self, plot, curve, x, y):
		curve.setData(x, y)
		plot.replot()

	def tiny_title(self, text, size=8):
		title = qwt.QwtText(text)
		title.setFont(Qt.QFont("Helvetica", size))
		return title

	def closeAcquire(self):
		self.i=0
		self.realTimeData=0
		self.timer.stop()
		try:
			self.file2.close()
		except:
			pass
		self.dataSpeedStep=0
		self.Nbstep=0 
		self.flagUpdate=True
		self.closeAcq=True
		self.actionSave_File.setCheckable(False)
		self.actionSave_File.setCheckable(True)
		self.actionSave_File.setIcon(self.iconSaveStop)
		
	def div_Speed(self,dataSpeed):
		#Mark
		Mark =255
		#start of data
		Id=0
		#Cmd=1 speed regulation
		Cmd=1
		SpeedmH=0
		SpeedmL=0
		TqH=0
		TqL=0
		d4H = 0
		d4L=0
		speedH,speedL=self.floatTo2byte(dataSpeed,1)
		DataFrameSpeed=[Mark,Id,Cmd,speedH,speedL,SpeedmH,SpeedmL,TqH,TqL,d4H,d4L]
		ck=self.checkSum(DataFrameSpeed)
		DataFrameSpeed.append(ck)
		print "Speed decrease!!"
		trameSpeed=self.trameCommand(DataFrameSpeed)
		cmd=trameSpeed.decode("hex")
		self.writeRS(ser,cmd)
		ser.flushInput #flush input buffer, discarding all its contents
		ser.flushOutput#flush output buffer, aborting current output
				 #and discard all that is in buffer


	def testCom(self,com,idDev):
		
		self.com=com
		portCom=""
		#print self.com
		for val in self.com:

			if(idDev==1):
				
				self.comRs232(val,baudMotor)
				DataFrameTest=[255,0,0,0,0,0,0,0,0,0,0,0]
				trameTest=self.trameCommand(DataFrameTest)
				cmd=trameTest.decode("hex")
				if(val!="/dev/ttyAMA0"):
					flagComIdev1=True
					self.writeRS(ser,cmd)
					dataFrame =ser.readlines(12)
					
					if (len(dataFrame)>0):
						frameDec=self.trameProcess(dataFrame)
						if frameDec[0]==255:
							print "Motor: OK!!"
							print "Motor serial port:"+val
							portCom=val
							flagComIdev1=False
							break
				
			elif (idDev==2):
				
				self.comRs232(val,baudSer)
				time.sleep(1)
				if(val!="/dev/ttyAMA0"):
					flagComIdev2=True
					xbeeFrame=ser.readline()
					if (len(xbeeFrame)>0):
						xbeeFrame1=xbeeFrame.split('\r\n')
						xbeeFrame2=xbeeFrame1[0]
						if xbeeFrame2[0]=="$":
							print "RF emitter: OK!!"
							print "RF serial port: "+val
							portCom=val
							flagComIdev2=False
							break
						
							

 
		if(idDev==1):
			
			if (flagComIdev1==True):
				print "ERROR :Check Motor Serial connection"
				self.showDialogError(idDev,flagComIdev1)
		if(idDev==2):
			
			if (flagComIdev2==True):
				print "ERROR :Check RF sensor emitter"
				self.flagNotemp=True
				self.showDialogError(idDev,flagComIdev2)
		
			
		ser.flushInput #flush input buffer, discarding all its contents
		ser.flushOutput#flush output buffer, aborting current output
			 #and discard all that is in buffer
		ser.close()
		return portCom
		
		
		

		
	def start_Acq(self):
		
		#test if data file exist
		self.fileDataExist()
		
		#resetting autoscale after zoom
		self.qwtPlotdata.setAxisAutoScale(qwt.QwtPlot.yLeft)
		self.qwtPlotdata.setAxisAutoScale(qwt.QwtPlot.yRight)
		self.qwtPlotdata.setAxisAutoScale(qwt.QwtPlot.xBottom)
		self.qwtPlotdata.setAxisAutoScale(qwt.QwtPlot.xTop)
		self.zoomers[0].setZoomBase(True)
		self.zoomers[1].setZoomBase(True)
		self.zoomers[2].setZoomBase(True)
		self.zoomers[3].setZoomBase(True)
		
		if(self.closeAcq==True):
			self.closeAcq=False
			self.showDialog()

		print "Acquisition starting"
		print self.Tacquisition
		
		self.timer.start(self.Tacquisition)

		self.flagStop=True
		
	def showDialog(self):
		#warning message when, the user restarting the acquisition
		#for the file of data
		msg= QtGui.QMessageBox()
		msg.setIcon(QtGui.QMessageBox.Warning)
		msg.setText("Do you want to save data in a new File?")
		msg.setWindowTitle("File data saving")
		msg.setStandardButtons(QtGui.QMessageBox.Ok|QtGui.QMessageBox.No)
		retval=msg.exec_()
		# QMessageBox.Ok= 0x00000400=1024(dec)
		if (retval == 1024):
			self.save_Data_File()

		else:
			try:
				self.file2 = open(self.filename_Data,'a+')
			except:
				pass
			
	def showDialogClose(self):
		#warning dialog when the user clicking on quit all button
		msg2= QtGui.QMessageBox()
		msg2= QtGui.QMessageBox()
		msg2.setIcon(QtGui.QMessageBox.Critical)
		msg2.setText("Are you sure to close the software")
		msg2.setWindowTitle("Close software")
		msg2.setStandardButtons(QtGui.QMessageBox.Ok|QtGui.QMessageBox.No)
		retval2=msg2.exec_()
		return retval2
		
	def showDialogError(self,idev,flag):
		#warning dialog when the user clicking on quit all button
		msg3= QtGui.QMessageBox()
		msg3= QtGui.QMessageBox()
		msg3.setIcon(QtGui.QMessageBox.Critical)
		if (idev==1):
			
			if (flag==True):
				msg3.setText("Do you want to continue without motor data?")
				msg3.setWindowTitle("ERROR:Motor board sensor")
		
		if(idev==2):
			if (flag==True):
				msg3.setText("Do you want to continue without temperature data?")
				msg3.setWindowTitle("ERROR:Temperature sensor")
			
		msg3.setStandardButtons(QtGui.QMessageBox.Yes|QtGui.QMessageBox.No)
		retval3=msg3.exec_()
		# QMessageBox.No= 0x0000100000=65536(dec)
		if (retval3 == 65536):
			print "exit"
			exit(1)
		return retval3
	
	
	
		
	def showDialogFile(self):
		#warning message when, the user starting the acquisition
		#for the file of data
		msg3= QtGui.QMessageBox()
		msg3.setIcon(QtGui.QMessageBox.Warning)
		msg3.setText("No file data\nCreate File ?")
		msg3.setWindowTitle("File data saving")
		msg3.setStandardButtons(QtGui.QMessageBox.Ok|QtGui.QMessageBox.No)
		retval=msg3.exec_()
		# QMessageBox.Ok= 0x00000400=1024(dec)
		if (retval == 1024):
			self.save_Data_File()
			
	def showMsgBtn(self):
		#warning message state of start manual button  
		msgBtn= QtGui.QMessageBox()
		msgBtn.setIcon(QtGui.QMessageBox.Warning)
		msgBtn.setText("Manual start button is ON!!\n Switch to the O position to continue")
		msgBtn.setWindowTitle("Manual start button state")
		msgBtn.setStandardButtons(QtGui.QMessageBox.Ok)
		retval=msgBtn.exec_()

		
	def closeAll(self):
		choice=self.showDialogClose()
		if (choice ==1024):
			self.stop_Motor()
			self.timer.stop()
			try:
				ser.close()
			except :
				pass
			self.close()
			GPIO.cleanup()
			
			
			
	def stop_Step(self):
		print "Stop Step"
		self.flagStep=False
		#self.flagStop=False
		self.flagdataStep=False
		#init index of step array
		self.i=-1
		self.dataSpeedStep=0
		#init index of joySpeed
		self.indexSpeed=4
		#init Icon
		self.actionSPEED_STEP.setCheckable(False)
		self.actionSPEED_STEP.setCheckable(True)
		self.actionSPEED_STEP.setIcon(self.iconStepStop)

	def stop_Motor(self):
		print "Motor Stop"
		#Mark
		self.flagStep=False
		self.flagStop=False
		self.flagdataStep=False
		Mark =255
		#start of data
		Id=0
		Cmd=3
		SpeedmH=0
		SpeedmL=0
		TqH=0
		TqL=0
		d4H = 0
		d4L=0
		speedH=0
		speedL=0
		DataFrameSpeed=[Mark,Id,Cmd,speedH,speedL,SpeedmH,SpeedmL,TqH,TqL,d4H,d4L]
		ck=self.checkSum(DataFrameSpeed)
		DataFrameSpeed.append(ck)
		trameSpeed=self.trameCommand(DataFrameSpeed)
		self.print_trame(trameSpeed)
		cmd=trameSpeed.decode("hex")
		self.writeRS(ser,cmd)
		self.writeRS(ser,cmd)
		ser.flushInput #flush input buffer, discarding all its contents
		ser.flushOutput#flush output buffer, aborting current output
		
	def init_Motor(self):
		#Mark
		Mark =255
		#start of data
		Id=0
		Cmd=0
		SpeedmH=0
		SpeedmL=0
		TqH=0
		TqL=0
		d4H = 0
		d4L=0
		speedH=0
		speedL=0
		DataFrameSpeed=[Mark,Id,Cmd,speedH,speedL,SpeedmH,SpeedmL,TqH,TqL,d4H,d4L]
		ck=self.checkSum(DataFrameSpeed)
		DataFrameSpeed.append(ck)
		trameSpeed=self.trameCommand(DataFrameSpeed)
		self.print_trame(trameSpeed)
		print "Init Motor"
		cmd=trameSpeed.decode("hex")
		self.writeRS(ser,cmd)
		self.writeRS(ser,cmd)
		ser.flushInput #flush input buffer, discarding all its contents
		ser.flushOutput#flush output buffer, aborting current output
		
	def open_file(self):
		self.speedData=[]
		self.dwellData=[]
		self.filename_Script=QtGui.QFileDialog.getOpenFileName(self,'Select file',dataFolder+scriptFolder)
		print self.filename_Script
		with open(self.filename_Script) as fileScr:
			
			
			#skip the first line , first line is the header
			next(fileScr)
			for line in fileScr:
				#get the first column : speed
				self.speedData.append(float(line.split(',')[0]))
				#get the second column : dwelltime
				self.dwellData.append(float(line.split(',')[1]))
				#self.stepMode.tableWidgetStep.setRowCount(2)

		#load speed value from file
		row=0
		
		self.stepMode.SpinBoxStep.setValue(len(self.speedData))
		for val in self.speedData:
			
			item=QtGui.QTableWidgetItem(str(val))
			self.stepMode.tableWidgetStep.setItem(row,0 , item)
			row+=1
			
		#load dwell time from file
		row=0
		for val in self.dwellData:
			
			item=QtGui.QTableWidgetItem(str(val))
			self.stepMode.tableWidgetStep.setItem(row,1 , item)
			row+=1

		print self.speedData
		print self.dwellData
		
	def loadScript(self):
		#selected the file
		self.filename_Script1=QtGui.QFileDialog.getOpenFileName(self,'Select file')
		dataX=[]
		dataY=[]
		dataTime=[]
		dataSpeed=[]
		
		listDataScript=[dataX,dataY]
		with open(self.filename_Script1) as fileScr:
			#skip the first line , first line is the header
			next(fileScr)
			for line in fileScr:
				for i in range(len(listDataScript)):
					#rstrip delete all \n
					listDataScript[i].append((line.rstrip('\n').split(',')[i]))
		
		dataTime=numpy.array(dataY,dtype=float)
		dataSpeed=numpy.array(dataX,dtype=float)
		maxSpeed=numpy.amax(dataSpeed)
		totalTime=numpy.sum(dataTime)
		timeNew=numpy.zeros(dataTime.size)
		timeStep=numpy.zeros((2*dataTime.size)+1)
		speedStep=numpy.zeros((2*dataTime.size)+1)
		print dataY
		print dataX
		print dataTime
		print dataSpeed
		timeNew[0]=dataTime[0]
		init=0.0
		for i in range(dataTime.size) :
			
			timeNew[i]=dataTime[i]+init
			init=timeNew[i]
		
		print  totalTime
		print  timeNew
		i=1
		
		timeStep[0]=0
		timeStep[1]=0
		
		while(i<(dataTime.size)):
			print i
			timeStep[2*i]=timeNew[i-1]
			timeStep[(2*i)+1]=timeNew[i-1]
			i+=1
		print timeStep
		
		j=0
		#while(j<dataTime.size):
			
		#	speedStep[2*j +1]=dataSpeed[j]
		#	speedStep[2*j +2]=dataSpeed[j]
		#	j+=1
		#speedStep[0]=0
		#speedStep[(2*dataTime.size) +1]=0
		#print SpeedStep
		#plotdata
		self.qwtPlotdata_2.xmin=0
		self.qwtPlotdata_2.xmax=totalTime
		self.qwtPlotdata_2.ymin=0
		self.qwtPlotdata_2.ymax=maxSpeed*(1.2)
		self.curve=QwtPlotCurve("Data from script speed")
		self.curve.attach(self.qwtPlotdata_2)
		#self.curve.setData(timeStep,speedStep)
		#self.qwtPlotdata_2.replot()
		return dataTime,dataSpeed
		
	def loadData(self):
	
		#data for lookup table
		dataDate=[]
		dataTime=[]
		dataSpeed=[]
		dataTorque=[]
		dataTemp=[]
		Nbcol=5
		Nbline=0
		i=0
		listData=[dataDate,dataTime,dataSpeed,dataTorque,dataTemp]
		self.filename_Script=QtGui.QFileDialog.getOpenFileName(self,'Select file')

		with open(self.filename_Script) as fileScr:
			
			
			#skip the first line , first line is the header
			next(fileScr)
			for line in fileScr:
				for i in range(Nbcol):
				#get date,time,speed,torque,temperature of each line
					listData[i].append((line.rstrip('\n').split(',')[i]))

				Nbline+=1
		#load value from file in cell

		self.tableWidgetData.setRowCount(Nbline)
		val=[]
		j=0
		for j in range(Nbcol):
			val=listData[j]

			# j=column
			for i in range(Nbline):
			 #i=row
				item=QtGui.QTableWidgetItem(str(val[i]))
				self.tableWidgetData.setItem(i,j , item)
				i+=1
			i=0

		#plot data when acquisition is off
		dataTime2=numpy.array(dataTime,dtype=float)
		dataSpeed2=numpy.array(dataSpeed,dtype=float)
		dataTorque2=numpy.array(dataTorque,dtype=float)
		dataTemp2=numpy.array(dataTemp,dtype=float)
		#maxSpeed=numpy.amax(dataSpeed)
		#totalTime=numpy.sum(dataTime)
		self.curveViewTq.attach(self.qwtviewPlot)
		self.curveViewTq.setData(dataTime2,dataTorque2)
		
		self.curveViewTp.attach(self.qwtviewPlot)
		self.curveViewTp.setData(dataTime2,dataTemp2)
		
		self.curveViewSp.attach(self.qwtviewPlot)
		self.curveViewSp.setData(dataTime2,dataSpeed2)
		self.qwtviewPlot.replot()

 #delete curve if checkbox is False
	def update_View(self):
		
		self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.yLeft)
		self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.yRight)
		self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.xBottom)
		self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.xTop)
		self.zoomers[2].setZoomBase(False)
		self.zoomers[3].setZoomBase(False)
		
		tp=self.checkBoxTempC.isChecked()
		tq=self.checkBoxTorque.isChecked()
		sp=self.checkBoxSpeed.isChecked()
		
		if (self.checkBoxTorque.isChecked()==False) :
			self.curveViewTq.detach()	
			self.qwtviewPlot.replot()
		else :
			self.curveViewTq.attach(self.qwtviewPlot)
			self.qwtviewPlot.replot()
			
		if (self.checkBoxTempC.isChecked()==False) :
			self.curveViewTp.detach()
			#Autoscale Second axis
			self.qwtviewPlot.enableAxis(qwt.QwtPlot.yRight)
			self.qwtviewPlot.setAxisTitle(qwt.QwtPlot.yRight, self.tiny_title("Speed[RPM]"))
			self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.yRight)
			self.qwtviewPlot.qwtviewPlot.replot()
		else :
			self.curveViewTp.attach(self.qwtviewPlot)
			self.qwtviewPlot.enableAxis(qwt.QwtPlot.yRight)
			self.qwtviewPlot.setAxisTitle(qwt.QwtPlot.yRight, self.tiny_title("Temperature("+degC+")"))
			self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.yRight)
			self.qwtviewPlot.replot()
		
		if (self.checkBoxSpeed.isChecked()==False) :
			self.curveViewSp.detach()
			self.qwtviewPlot.enableAxis(qwt.QwtPlot.yRight)
			self.qwtviewPlotsetAxisTitle(qwt.QwtPlot.yRight, self.tiny_title("Temperature("+degC+")"))
			self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.yRight)
			self.qwtviewPlot.replot()
		else :
			self.curveViewSp.attach(self.qwtviewPlot)
			self.qwtviewPlot.enableAxis(qwt.QwtPlot.yRight)
			self.qwtviewPlot.setAxisTitle(qwt.QwtPlot.yRight, self.tiny_title("Speed[RPM]"))
			self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.yRight)
			self.qwtviewPlot.replot()
		
		if ((self.checkBoxTempC.isChecked()==True) and (self.checkBoxSpeed.isChecked()==True)):
			self.qwtviewPlot.enableAxis(qwt.QwtPlot.yRight)
			self.qwtviewPlot.setAxisTitle(qwt.QwtPlot.yRight, self.tiny_title("Speed-Temperature"))
			self.qwtviewPlot.setAxisAutoScale(qwt.QwtPlot.yRight)
		#script file
	def save_Script_File(self):
		print "SaveFile"
		self.filename_Script=QtGui.QFileDialog.getSaveFileName(self,'Select file')
		print self.filename_Script
		file1 = open(self.filename_Script,'w') 
		#header of script file
		file1.write("Speed(rpm),Dwell time (s)\n")
		i=0
		#call load_Cell to load data from table
		self.load_Cell()
		#save data of script
		for i in range (len(self.speedCell)):
			file1.write(str(self.speedCell[i])+','+str(self.dwellTimeCell[i])+'\n')
		file1.close
		
		#data file
	def save_Data_File(self):
		dateFile=datetime.datetime.utcnow().strftime("%d_%m_%y_%H_%M")
		defaultName="data"+dateFile+".txt"
		print "File of data:"
		self.filename_Data=QtGui.QFileDialog.getSaveFileName(self,'Select file',dataFolder+defaultName)
		if (self.filename_Data):
			print "DATA SAVING"
			self.setIconSave()
		else:
			print "NO SAVING DATA"
			
		print "File Name:"+self.filename_Data
		self.file2 = open(self.filename_Data,'a+') 
		if (os.path.getsize(self.filename_Data) == 0):
			#header of script file
			self.file2.write("Date,Dwell time (s),Speed(rpm),Torque(mN.m),Temperature(degC)\n")
		print self.filename_Data
		
	def write_dataToFile(self,fileName,date,dwelltime,speed,torque,temperature):
		
		dataStr=date+','+str(dwelltime)+','+str("%.2f"%speed)+','+str("%.6f"%torque)+','+str("%.2f"%temperature)+'\n'
		try:
			self.file2.write(dataStr)
		except:
			pass
			
	def fileDataExist(self):
		
		try:
			os.path.isfile(self.filename_Data)
			print "File exist"
		except:
			self.showDialogFile()
			
			
	
			
		
		#list serial port
	def list_serial_port(self):
		""" Lists serial port names

		:raises EnvironmentError:
			On unsupported or unknown platforms
		:returns:
			A list of the serial ports available on the system
	"""
		#print "List serial port !!!"
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
		# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		result=[]
		
		for port in ports:
			try:
				
				s = serial.Serial(port)
				s.close()
				result.append(port)
				
			except (OSError, serial.SerialException):
				pass

		return result
		
	def init_Combox(self,listStr=[]):
		#Add value in the combox
		self.comboBoxComport.addItems(listStr)
		
	def update_com(self):
		
		self.listComPort=self.list_serial_port()
		print self.listComPort
		#clear old value and put new value
		self.comboBoxComport.clear()
		self.init_Combox(self.listComPort)
		
	def setIndexCom(self,com):
		
		index = self.comboBoxComport.findText(com, QtCore.Qt.MatchFixedString)
		if index >= 0:
			self.comboBoxComport.setCurrentIndex(index)
		
		
	def comRs232(self,comPort,baud):
		
		try:
			#config rs232 8N1
				ser.port = comPort
				ser.baudrate = baud
				ser.timeout=0
				ser.open()
			
		except:
			pass
		
		

	def writeRS(self,ser,cmd):

		
		ser.flushInput #flush input buffer, discarding all its contents
		ser.flushOutput#flush output buffer, aborting current output
				 #and discard all that is in buffer
		#self.ser.open()
		ser.write(cmd)
		time.sleep(0.1)  #give the serial port sometime to receive the data
		#data=ser.readlines()
		#print"Read data: {0} ".format(data)



	def acqData(self,ser,cmd):

		while(ser.inWaiting())== 0:
			writeRS(ser,cmd)
		
			




	def float_to_hex(self,f):
		return hex(struct.unpack('<I', struct.pack('<f', f))[0])
		
		
	def trameProcess(self,trameList):
			
			#convert list to string
			dataStr=''.join(trameList)
			dataDec=[]
			#convert string to a list of decimal value
			for data in range(len(dataStr)):
				dataDec.append(ord(dataStr[data]))
			return dataDec
			

	def decToHexa(self,data):
		
		dataOut="0x{:02x}".format(data)
		return dataOut[2:]

	def trameCommand(self,dataFrameCd):
		data=''
		for i in range(len(dataFrameCd)):
			
			data+= self.decToHexa(dataFrameCd[i])
		return data
		
	def floatTo2byte(self,data,val):
			intdata=int(abs(data))
			i=val
			#if i=1  speed measurement
			#convert a float to 2 byte
			#b15=1 sign +
			#b15=0 sign -
			
			#b14 to b6 : integer data on 9 bits
			#b5 to b0  : fractionnal part of data
			
			
			#if i=2 torque measurement
			#convert a float to 2 byte
			#No sign bit
			
			#b14 to b15 : integer data on 2 bits
			#b13 to b0  : fractionnal part of data

			
			if(i==1):
				Nbit=6  #numbers of decimal
				#format to 010 : 10 digits, 0 if bit=0
				bindata=format(intdata,'09b')
				
			else:
				Nbit=14
				#format to 010 : 14 digits, 0 if bit=0
				bindata=format(intdata,'02b')

			

				#Data Sign
			if(data<0):
				bitSign=1
			else:
				bitSign=0
				
		 #Integer part to binary
		 
			#format to 010 : N digits, 0 if bit=0
			listBin=[]
			data16Bits=[]
			#put b15 bit
			if (val == 1):
				data16Bits.append(bitSign)
			
			#need to create a list of binary 
			for x in range(len(bindata)):
			
				listBin.append(int(bindata[x]))

			#put each bit of integer part data 
			for x in listBin:
			
				data16Bits.append(x)

			#get fractionnal part of data
			fracdata=abs(data)-numpy.fix(abs(data))
			
			#calculate the binary value of fractionnal 
			tabBit=[]

			for i in range (Nbit):
				temp=fracdata*2
				if (temp>1):
					tabBit.append(1)
					fracdata=temp-1
				else:
					tabBit.append(0)
					fracdata=temp
			#put each bit of fractionnal 
			for x in tabBit:
				data16Bits.append(x)
			print "data16bits",data16Bits

			data16BitsHigh=data16Bits[:8]
			
			data16BitsLow=data16Bits[-8:]



			highBitsToDec=int("".join(map(str,data16BitsHigh)),2)


			lowBitsToDec=int("".join(map(str,data16BitsLow)),2)


			return highBitsToDec,lowBitsToDec

		
		
	def byteTofloat(self,highBytes,LowBytes,val):
		sumFrac=0.0
		#format data in 8 bits
		high=format(highBytes,'08b')
		low=format(LowBytes,'08b')
		
		#Create 16 bits data
		data16Str=high+low
		listBin2=[]
		dataInt=[]
		for i in range(len(data16Str)):
			listBin2.append(int(data16Str[i]))
		if (val==1):
			
			if(int(listBin2[0])==1):
				sign=-1
			
			else:
				sign=1
			

		if val==1:

			#speed measurement
			Nbit=6 #number of decimal
			dataInt=listBin2[1:10]
			dataFrac=listBin2[10:]
			
			
		if val==2:
			Nbit=14 #number of decimal
			#torque measurement
			dataInt=listBin2[0:2]
			dataFrac=listBin2[2:]

		dataDec=int("".join(map(str,dataInt)),2)
		for i in range(Nbit):
			exp=2**((-1*(i+1)))
			sumFrac+=dataFrac[i]*exp
		if (val ==1):
			dataD=(dataDec+sumFrac)*sign
		else:
			
			dataD=(dataDec+sumFrac)
		return dataD
		
	def checkSum(self,trame):
		ck = 0
		i=0
		while(i< len(trame)):
			ck=trame[i]+ck
			i+=1
		
		ck=ck%256
		return ck
		
	def print_trame(sel,trame):
		trameStr =""

		for i in range(len (trame)):

			trameStr=trameStr+str(trame[i])+"-"
		print"trame:",trameStr[:-1]
		
	def initPicker(self):
		yCursor=[qwt.QwtPlot.yRight,qwt.QwtPlot.yLeft]
		if(self.radioButtonSpeed.isChecked()):
			cursor=yCursor[0]
		elif (self.radioButtonTorque.isChecked()):
			cursor=yCursor[1]
		else:
			cursor=yCursor[1]
		self.picker = qwt.QwtPlotPicker(
		qwt.QwtPlot.xBottom,
		cursor,
		qwt.QwtPicker.PointSelection |qwt.QwtPicker.DragSelection,
		qwt.QwtPlotPicker.CrossRubberBand,
		qwt.QwtPicker.AlwaysOn ,
		self.qwtPlotdata.canvas())
		self.picker.setRubberBandPen(Qt.QPen(Qt.Qt.green))
		self.picker.setTrackerPen(Qt.QPen(Qt.Qt.cyan))
		
		#picker for 2nd plot
		
		self.picker2 = qwt.QwtPlotPicker(
		qwt.QwtPlot.xBottom,
		cursor,
		qwt.QwtPicker.PointSelection |qwt.QwtPicker.DragSelection,
		qwt.QwtPlotPicker.CrossRubberBand,
		qwt.QwtPicker.AlwaysOn ,
		self.qwtPlotDataZoom.canvas())
		self.picker2.setRubberBandPen(Qt.QPen(Qt.Qt.green))
		self.picker2.setTrackerPen(Qt.QPen(Qt.Qt.cyan))
		
		#picker for third plot
		
		self.picker3 = qwt.QwtPlotPicker(
		qwt.QwtPlot.xBottom,
		cursor,
		qwt.QwtPicker.PointSelection |qwt.QwtPicker.DragSelection,
		qwt.QwtPlotPicker.CrossRubberBand,
		qwt.QwtPicker.AlwaysOn ,
		self.qwtviewPlot.canvas())
		self.picker3.setRubberBandPen(Qt.QPen(Qt.Qt.green))
		self.picker3.setTrackerPen(Qt.QPen(Qt.Qt.cyan))
		
		self.showInfo('Cursor Pos: Press left mouse button in plot region')
		self.connect(self.picker,QtCore.SIGNAL('moved(const QPoint &)'),self.moved)
		self.connect(self.picker2,QtCore.SIGNAL('moved(const QPoint &)'),self.moved)
		self.connect(self.picker3,QtCore.SIGNAL('moved(const QPoint &)'),self.moved)
		
	def clearPicker(self):
		#need to clear pick if not label will be superimpose
		self.picker.setEnabled(False)
		self.picker2.setEnabled(False)
		self.picker3.setEnabled(False)
		#call initPicker() to update cursors
		self.initPicker()
		
	
	def initZoomer(self,plot):
		
		self.zoomers = []
		zoomer = qwt.QwtPlotZoomer(
			qwt.QwtPlot.xBottom,
			qwt.QwtPlot.yLeft,
			qwt.QwtPicker.DragSelection,
			qwt.QwtPicker.AlwaysOff,
			plot[0].canvas())
		zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))
		self.zoomers.append(zoomer)

		zoomer = qwt.QwtPlotZoomer(
			qwt.QwtPlot.xTop,
			qwt.QwtPlot.yRight,
			qwt.QwtPicker.PointSelection | qwt.QwtPicker.DragSelection,
			qwt.QwtPicker.AlwaysOn,
			plot[0].canvas())
		zoomer.setRubberBand(qwt.QwtPicker.NoRubberBand)
		
		self.zoomers.append(zoomer)
		
		zoomer = qwt.QwtPlotZoomer(
			qwt.QwtPlot.xBottom,
			qwt.QwtPlot.yLeft,
			qwt.QwtPicker.DragSelection,
			qwt.QwtPicker.AlwaysOff,
			plot[1].canvas())
		zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))
		self.zoomers.append(zoomer)

		zoomer = qwt.QwtPlotZoomer(
			qwt.QwtPlot.xTop,
			qwt.QwtPlot.yRight,
			qwt.QwtPicker.PointSelection | qwt.QwtPicker.DragSelection,
			qwt.QwtPicker.AlwaysOn,
			plot[1].canvas())
		zoomer.setRubberBand(qwt.QwtPicker.NoRubberBand)
		
		self.zoomers.append(zoomer)
		
		zoomer = qwt.QwtPlotZoomer(
			qwt.QwtPlot.xTop,
			qwt.QwtPlot.yLeft,
			qwt.QwtPicker.DragSelection,
			qwt.QwtPicker.AlwaysOn,
			plot[1].canvas())
		zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))
		
		
		self.zoomers.append(zoomer)
		
		
	def zoom(self, on):
		
		self.zoomers[0].setEnabled(on)
		self.zoomers[0].zoom(0)
		
		self.zoomers[1].setEnabled(on)
		self.zoomers[1].zoom(0)
		
		self.zoomers[2].setEnabled(on)
		self.zoomers[2].zoom(0)
		
		self.zoomers[3].setEnabled(on)
		self.zoomers[3].zoom(0)

		if on:
			self.picker.setRubberBand(qwt.QwtPicker.NoRubberBand)
			self.picker2.setRubberBand(qwt.QwtPicker.NoRubberBand)
			self.picker3.setRubberBand(qwt.QwtPicker.NoRubberBand)
		else:
			self.picker.setRubberBand(qwt.QwtPicker.CrossRubberBand)
			self.picker2.setRubberBand(qwt.QwtPicker.CrossRubberBand)
			self.picker3.setRubberBand(qwt.QwtPicker.CrossRubberBand)
		self.update_View()
		self.showInfo()

    # zoom()

	def showInfo(self, text=None):
		if not text:
			if self.picker.rubberBand()  :
				text = 'Cursor Pos: Press left mouse button in plot region'
				
			if self.picker2.rubberBand()  :
				text = 'Cursor Pos: Press left mouse button in plot region 2'
				
			else:
				text = " "
				
		self.statusBar().showMessage(text)
				
	# showInfo()
	
	def moved(self, point):
		
		
		
		if(self.tabWidgetIHM.currentIndex()==0):
			
			self.zoomers[2].setEnabled(False)
			self.picker3.setRubberBand(qwt.QwtPicker.NoRubberBand)
			if(self.radioButtonSpeed.isChecked()):

				info = "Time(ms)=%g,Torque(mN.m)=%0.2f,Speed(rpm)=%0.2f" % (
				self.qwtPlotdata.invTransform(qwt.QwtPlot.xBottom, point.x()),
				self.qwtPlotdata.invTransform(qwt.QwtPlot.yLeft, point.y()),
				self.qwtPlotdata.invTransform(qwt.QwtPlot.yRight, point.y()))
		
			if(self.radioButtonTorque.isChecked()):
				
				info = "Time(ms)=%g,Torque(mN.m)=%0.2f,Speed(rpm)=%0.2f" % (
				self.qwtPlotdata.invTransform(qwt.QwtPlot.xBottom, point.x()),
				self.qwtPlotdata.invTransform(qwt.QwtPlot.yLeft, point.y()),
				self.qwtPlotdata.invTransform(qwt.QwtPlot.yRight, point.y()))
			
		if(self.tabWidgetIHM.currentIndex()==1):
			
			self.zoomers[0].setEnabled(False)
			self.picker.setRubberBand(qwt.QwtPicker.NoRubberBand)
			self.zoomers[1].setEnabled(False)
			self.picker2.setRubberBand(qwt.QwtPicker.NoRubberBand)
			
			if(self.radioButtonSpeed.isChecked()):

				info = "Time(ms)=%g,Torque(mN.m)=%0.2f,Speed(rpm)=%0.2f" % (
				self.qwtviewPlot.invTransform(qwt.QwtPlot.xBottom, point.x()),
				self.qwtviewPlot.invTransform(qwt.QwtPlot.yRight, point.y()),
				self.qwtviewPlot.invTransform(qwt.QwtPlot.yLeft, point.y()))
		
			if(self.radioButtonTorque.isChecked()):
			
				info = "Time(ms)=%g,Torque(mN.m)=%0.2f,Speed=%0.2f" % (
				self.qwtviewPlot.invTransform(qwt.QwtPlot.xBottom, point.x()),
				self.qwtviewPlot.invTransform(qwt.QwtPlot.yRight, point.y()),
				self.qwtviewPlot.invTransform(qwt.QwtPlot.yLeft, point.y()))
		
		self.showInfo(info)

	# moved()
	
	
	def selected(self,_):
		self.showInfo()

	# selected()

	def initGpio(self,channel):
		
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(channel,GPIO.IN)
		GPIO.setup(channel,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	
	def callBackOn(self,self_):
		
		
		if (GPIO.input(onOff)==0):
			#flag manual button
			self.manBut=True
			self.actionSTOP_MOTOR.setChecked(True)
			self.actionSTOP_MOTOR.setIcon(self.iconStop)
			#start at 1 tr/minonOff
			#if(self.flagStep==False):
			self.speedDia.SpeedControl.setValue(speedStart)
			self.update_Speed()

		else :
			self.manBut=False
			self.actionSTOP_MOTOR.setChecked(False)
			self.actionSTOP_MOTOR.setIcon(self.iconRun)
			self.actionSPEED_STEP.setCheckable(False)
			self.actionSPEED_STEP.setCheckable(True)
			self.actionSPEED_STEP.setIcon(self.iconStepStop)
			#init index of step array
			self.i=-1
			self.dataSpeedStep=0
			#init index of joySpeed
			self.indexSpeed=4
			self.stop_Motor()
			
	def callBackPlus(self,self_):
		self.manBut=True
		if ((GPIO.input(incSp)==0)and((GPIO.input(onOff)==0)or(self.flagStop==True))):
			#stop speed step if joystick on
			if (self.flagStep==True):
				self.stop_Step()
			print "SPEED++"
			self.indexSpeed+=1
			print "****INDEX*****:",self.indexSpeed
			
			if (self.indexSpeed > (len(self.tabJoySpeed) - 1) ):
				self.indexSpeed=self.indexSpeed - 1
				print "****INDEX*****:",self.indexSpeed
				print "Max Speed has been reach !!"
				self.speedPlus()
			else:
				
				self.speedPlus()
			#self.speedPlus()
		
	def callBackMinus(self,self_):
		self.manBut==True
		if (GPIO.input(decSp)==0):
			if (self.flagStep==True):
				#stop speed step if joystick on
				self.stop_Step()
			print "SPEED--"
			if (self.indexSpeed==0):
				print "INDEX min has been reach!!"
				print "****INDEX*****:",self.indexSpeed
		
			else :
				self.indexSpeed-=1
				print "****INDEX*****:",self.indexSpeed
				if (self.indexSpeed < 0):
					print "Min Speed has been reach !!"
					self.indexSpeed=self.indexSpeed+1
					self.speedMinus()
				else:
					self.speedMinus()
		
		


class stepDialog(QtGui.QDialog,Step_Ui_Dialog):
	def __init__(self,parent=None):
		super(stepDialog, self).__init__(parent)
		self.setupUi(self)

class speedDialog(QtGui.QDialog,Speed_Ui_Dialog,Ui_MainWindow):
	def __init__(self,parent=None):
		super(speedDialog, self).__init__(parent)
		self.setupUi(self)
	def closeEvent(self,event):
		self.parent().actionSTOP_MOTOR.setIcon(self.parent().iconRun)
		#disable speed fix command , need False and after true
		#use self.parent to use herit function
		self.parent().actionSPEED_FIX.setCheckable(False)
		self.parent().actionSPEED_FIX.setCheckable(True)
		#stop motor
		self.parent().stop_Motor()
		self.parent().actionSTOP_MOTOR.setCheckable(False)
		self.parent().actionSTOP_MOTOR.setCheckable(True)
		#Init fix speed dialog
		self.parent().speedDia.SpeedControl.setValue(speedStart)


def main(argv):
	app = QtGui.QApplication(argv)
	
	
	#QcleanlookStyle
	app.setStyle('windows vista')
	QtCore.QObject.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app,QtCore.SLOT("quit()"))
	window = MyForm()
	window.initGpio(onOff)
	window.initGpio(incSp)
	window.initGpio(decSp)
	window.stateOfStart()
	GPIO.add_event_detect(onOff,GPIO.FALLING,callback=window.callBackOn)
	GPIO.add_event_detect(incSp,GPIO.FALLING,callback=window.callBackPlus,bouncetime=500)
	GPIO.add_event_detect(decSp,GPIO.FALLING,callback=window.callBackMinus,bouncetime=300)
	#window.showFullScreen()
	window.show()
	app.exec_()


if __name__ == "__main__":
	main(sys.argv)

