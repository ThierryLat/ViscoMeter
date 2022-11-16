#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import Qt, QtCore, QtGui
import PyQt4.Qwt5 as qwt
from PyQt4.Qwt5 import QwtPlotCurve
#from qwt_plot_curve import QwtPlotCurve

from windowTime import Ui_MainWindow # created with QtDesigner and pyuic
from datetime import datetime
import sys
import os

class MyForm(QtGui.QMainWindow,Ui_MainWindow):
	
	def __init__(self,parent=None):
		super(MyForm, self).__init__(parent)
		#QtGui.QMainWindow.__init__(self)
		#self.ui = Ui_MainWindow()  # created with QtDesigner and pyuic
		self.setupUi(self)
		
		#slot signal
		########################
		self.pushButtonSetTime.clicked.connect(self.getDate)
		self.timeEdit.setDisplayFormat("hh:mm:ss")
		self.timeEdit.setTime(QtCore.QTime.currentTime())

	def getDate(self):
	
		mdate=self.calendarWidget.selectedDate()
		mtime=self.timeEdit.time()
		mHour=mtime.hour()
		mMinute=mtime.minute()
		mSecond=mtime.second()
		mYear=mdate.year()
		mMonth=mdate.month()
		mDate=mdate.day()
		date_obj=datetime(mYear,mMonth,mDate,mHour,mMinute,mSecond)
		setdate="sudo date --set="+"'"+str(date_obj)+"'"
		#instalRtc="sudo bash /home/pi/install-piface-real-time-clock.sh"
		setHwclock="sudo hwclock -w"
		#reboot="sudo reboot -f"
		print setdate
		#print instalRtc
		print setHwclock
		print date_obj
		os.system(setdate)
		#os.system(instalRtc)
		os.system(setHwclock)
		#os.system(reboot)


def main(argv):
	app = QtGui.QApplication(argv)
	#QcleanlookStyle
	app.setStyle('windows vista')
	QtCore.QObject.connect(app, QtCore.SIGNAL("lastWindowClosed()"), app,QtCore.SLOT("quit()"))
	window = MyForm()
	window.show()
	app.exec_()


if __name__ == "__main__":
	main(sys.argv)
