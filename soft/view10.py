# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_pi7.ui'
#
# Created: Fri Aug 27 15:13:17 2021
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(780, 440)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(780, 400))
        font = QtGui.QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidgetIHM = QtGui.QTabWidget(self.centralwidget)
        self.tabWidgetIHM.setGeometry(QtCore.QRect(10, 50, 751, 311))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidgetIHM.sizePolicy().hasHeightForWidth())
        self.tabWidgetIHM.setSizePolicy(sizePolicy)
        self.tabWidgetIHM.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidgetIHM.setObjectName(_fromUtf8("tabWidgetIHM"))
        self.tabAcquisition = QtGui.QWidget()
        self.tabAcquisition.setObjectName(_fromUtf8("tabAcquisition"))
        self.verticalLayoutWidget = QtGui.QWidget(self.tabAcquisition)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 0, 731, 281))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.qwtPlotdata = Qwt5.QwtPlot(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qwtPlotdata.sizePolicy().hasHeightForWidth())
        self.qwtPlotdata.setSizePolicy(sizePolicy)
        self.qwtPlotdata.setMinimumSize(QtCore.QSize(0, 0))
        self.qwtPlotdata.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.qwtPlotdata.setObjectName(_fromUtf8("qwtPlotdata"))
        self.verticalLayout_3.addWidget(self.qwtPlotdata)
        self.qwtPlotDataZoom = Qwt5.QwtPlot(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qwtPlotDataZoom.sizePolicy().hasHeightForWidth())
        self.qwtPlotDataZoom.setSizePolicy(sizePolicy)
        self.qwtPlotDataZoom.setMinimumSize(QtCore.QSize(200, 0))
        self.qwtPlotDataZoom.setObjectName(_fromUtf8("qwtPlotDataZoom"))
        self.verticalLayout_3.addWidget(self.qwtPlotDataZoom)
        self.tabWidgetIHM.addTab(self.tabAcquisition, _fromUtf8(""))
        self.Look = QtGui.QWidget()
        self.Look.setObjectName(_fromUtf8("Look"))
        self.horizontalLayoutWidget_3 = QtGui.QWidget(self.Look)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 661, 281))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.horizontalLayoutCurve = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayoutCurve.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayoutCurve.setMargin(0)
        self.horizontalLayoutCurve.setObjectName(_fromUtf8("horizontalLayoutCurve"))
        self.qwtviewPlot = Qwt5.QwtPlot(self.horizontalLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qwtviewPlot.sizePolicy().hasHeightForWidth())
        self.qwtviewPlot.setSizePolicy(sizePolicy)
        self.qwtviewPlot.setMaximumSize(QtCore.QSize(16777210, 16777215))
        self.qwtviewPlot.setObjectName(_fromUtf8("qwtviewPlot"))
        self.horizontalLayoutCurve.addWidget(self.qwtviewPlot)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.Look)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(660, 0, 61, 261))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.checkBoxSpeed = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBoxSpeed.setChecked(True)
        self.checkBoxSpeed.setObjectName(_fromUtf8("checkBoxSpeed"))
        self.verticalLayout_2.addWidget(self.checkBoxSpeed)
        self.checkBoxTorque = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBoxTorque.setChecked(True)
        self.checkBoxTorque.setObjectName(_fromUtf8("checkBoxTorque"))
        self.verticalLayout_2.addWidget(self.checkBoxTorque)
        self.checkBoxTempC = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.checkBoxTempC.setChecked(True)
        self.checkBoxTempC.setObjectName(_fromUtf8("checkBoxTempC"))
        self.verticalLayout_2.addWidget(self.checkBoxTempC)
        self.pushButtonLoadData = QtGui.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonLoadData.sizePolicy().hasHeightForWidth())
        self.pushButtonLoadData.setSizePolicy(sizePolicy)
        self.pushButtonLoadData.setMinimumSize(QtCore.QSize(0, 50))
        self.pushButtonLoadData.setObjectName(_fromUtf8("pushButtonLoadData"))
        self.verticalLayout_2.addWidget(self.pushButtonLoadData)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.tabWidgetIHM.addTab(self.Look, _fromUtf8(""))
        self.tabLookup = QtGui.QWidget()
        self.tabLookup.setObjectName(_fromUtf8("tabLookup"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.tabLookup)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 0, 691, 281))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.tableWidgetData = QtGui.QTableWidget(self.horizontalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetData.sizePolicy().hasHeightForWidth())
        self.tableWidgetData.setSizePolicy(sizePolicy)
        self.tableWidgetData.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableWidgetData.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidgetData.setAutoScroll(True)
        self.tableWidgetData.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.tableWidgetData.setObjectName(_fromUtf8("tableWidgetData"))
        self.tableWidgetData.setColumnCount(5)
        self.tableWidgetData.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetData.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetData.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetData.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetData.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetData.setHorizontalHeaderItem(4, item)
        self.horizontalLayout_3.addWidget(self.tableWidgetData)
        self.tabWidgetIHM.addTab(self.tabLookup, _fromUtf8(""))
        self.tabAnalysis = QtGui.QWidget()
        self.tabAnalysis.setObjectName(_fromUtf8("tabAnalysis"))
        self.groupBoxCmdMotor = QtGui.QGroupBox(self.tabAnalysis)
        self.groupBoxCmdMotor.setGeometry(QtCore.QRect(0, 20, 731, 291))
        self.groupBoxCmdMotor.setObjectName(_fromUtf8("groupBoxCmdMotor"))
        self.gridLayoutWidget = QtGui.QWidget(self.groupBoxCmdMotor)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(50, 30, 611, 165))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.radioButtonSpeed = QtGui.QRadioButton(self.gridLayoutWidget)
        self.radioButtonSpeed.setCheckable(True)
        self.radioButtonSpeed.setChecked(True)
        self.radioButtonSpeed.setObjectName(_fromUtf8("radioButtonSpeed"))
        self.gridLayout.addWidget(self.radioButtonSpeed, 0, 4, 1, 1)
        self.comboBoxComport = QtGui.QComboBox(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxComport.sizePolicy().hasHeightForWidth())
        self.comboBoxComport.setSizePolicy(sizePolicy)
        self.comboBoxComport.setObjectName(_fromUtf8("comboBoxComport"))
        self.gridLayout.addWidget(self.comboBoxComport, 6, 4, 1, 2)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.TorqueTreshTimedoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TorqueTreshTimedoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.TorqueTreshTimedoubleSpinBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.TorqueTreshTimedoubleSpinBox.setFont(font)
        self.TorqueTreshTimedoubleSpinBox.setSpecialValueText(_fromUtf8(""))
        self.TorqueTreshTimedoubleSpinBox.setMaximum(2500.0)
        self.TorqueTreshTimedoubleSpinBox.setProperty("value", 2200.0)
        self.TorqueTreshTimedoubleSpinBox.setObjectName(_fromUtf8("TorqueTreshTimedoubleSpinBox"))
        self.gridLayout.addWidget(self.TorqueTreshTimedoubleSpinBox, 3, 4, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
        self.radioButtonTorque = QtGui.QRadioButton(self.gridLayoutWidget)
        self.radioButtonTorque.setObjectName(_fromUtf8("radioButtonTorque"))
        self.gridLayout.addWidget(self.radioButtonTorque, 0, 5, 1, 1)
        self.radioButtonTemperature = QtGui.QRadioButton(self.gridLayoutWidget)
        self.radioButtonTemperature.setObjectName(_fromUtf8("radioButtonTemperature"))
        self.gridLayout.addWidget(self.radioButtonTemperature, 0, 6, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 1, 1, 1)
        self.WindowTimedoubleSpinBox = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WindowTimedoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.WindowTimedoubleSpinBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.WindowTimedoubleSpinBox.setFont(font)
        self.WindowTimedoubleSpinBox.setSpecialValueText(_fromUtf8(""))
        self.WindowTimedoubleSpinBox.setMaximum(3600.0)
        self.WindowTimedoubleSpinBox.setProperty("value", 10.0)
        self.WindowTimedoubleSpinBox.setObjectName(_fromUtf8("WindowTimedoubleSpinBox"))
        self.gridLayout.addWidget(self.WindowTimedoubleSpinBox, 4, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 6, 7, 1, 1)
        self.labelComPort = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelComPort.sizePolicy().hasHeightForWidth())
        self.labelComPort.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelComPort.setFont(font)
        self.labelComPort.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.labelComPort.setObjectName(_fromUtf8("labelComPort"))
        self.gridLayout.addWidget(self.labelComPort, 6, 1, 1, 1)
        self.toolButtonUpdateCom = QtGui.QToolButton(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButtonUpdateCom.sizePolicy().hasHeightForWidth())
        self.toolButtonUpdateCom.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.toolButtonUpdateCom.setFont(font)
        self.toolButtonUpdateCom.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolButtonUpdateCom.setObjectName(_fromUtf8("toolButtonUpdateCom"))
        self.gridLayout.addWidget(self.toolButtonUpdateCom, 6, 6, 1, 1)
        self.labelComPort_2 = QtGui.QLabel(self.gridLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelComPort_2.sizePolicy().hasHeightForWidth())
        self.labelComPort_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelComPort_2.setFont(font)
        self.labelComPort_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.labelComPort_2.setObjectName(_fromUtf8("labelComPort_2"))
        self.gridLayout.addWidget(self.labelComPort_2, 2, 1, 1, 1)
        self.comboBoxGear = QtGui.QComboBox(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboBoxGear.setFont(font)
        self.comboBoxGear.setEditable(False)
        self.comboBoxGear.setObjectName(_fromUtf8("comboBoxGear"))
        self.comboBoxGear.addItem(_fromUtf8(""))
        self.comboBoxGear.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxGear, 2, 4, 1, 1)
        self.tabWidgetIHM.addTab(self.tabAnalysis, _fromUtf8(""))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 751, 42))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelSpeed = QtGui.QLabel(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSpeed.sizePolicy().hasHeightForWidth())
        self.labelSpeed.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelSpeed.setFont(font)
        self.labelSpeed.setObjectName(_fromUtf8("labelSpeed"))
        self.horizontalLayout.addWidget(self.labelSpeed)
        self.lineEditSpeed = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditSpeed.sizePolicy().hasHeightForWidth())
        self.lineEditSpeed.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEditSpeed.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Technic"))
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditSpeed.setFont(font)
        self.lineEditSpeed.setText(_fromUtf8(""))
        self.lineEditSpeed.setObjectName(_fromUtf8("lineEditSpeed"))
        self.horizontalLayout.addWidget(self.lineEditSpeed)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.labelTorque = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelTorque.setFont(font)
        self.labelTorque.setObjectName(_fromUtf8("labelTorque"))
        self.horizontalLayout.addWidget(self.labelTorque)
        self.lineEditTorque = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTorque.sizePolicy().hasHeightForWidth())
        self.lineEditTorque.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 173, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 173, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEditTorque.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Technic"))
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditTorque.setFont(font)
        self.lineEditTorque.setText(_fromUtf8(""))
        self.lineEditTorque.setObjectName(_fromUtf8("lineEditTorque"))
        self.horizontalLayout.addWidget(self.lineEditTorque)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.labelTemperature = QtGui.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelTemperature.setFont(font)
        self.labelTemperature.setObjectName(_fromUtf8("labelTemperature"))
        self.horizontalLayout.addWidget(self.labelTemperature)
        self.lineEditTemperature = QtGui.QLineEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditTemperature.sizePolicy().hasHeightForWidth())
        self.lineEditTemperature.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lineEditTemperature.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Technic"))
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.lineEditTemperature.setFont(font)
        self.lineEditTemperature.setText(_fromUtf8(""))
        self.lineEditTemperature.setObjectName(_fromUtf8("lineEditTemperature"))
        self.horizontalLayout.addWidget(self.lineEditTemperature)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSTART_ACQ = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/play.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSTART_ACQ.setIcon(icon)
        self.actionSTART_ACQ.setObjectName(_fromUtf8("actionSTART_ACQ"))
        self.actionSTOP_Plot = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSTOP_Plot.setIcon(icon1)
        self.actionSTOP_Plot.setObjectName(_fromUtf8("actionSTOP_Plot"))
        self.actionSave_File = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_File.setIcon(icon2)
        self.actionSave_File.setObjectName(_fromUtf8("actionSave_File"))
        self.actionQUIT_ALL = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/exit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQUIT_ALL.setIcon(icon3)
        self.actionQUIT_ALL.setObjectName(_fromUtf8("actionQUIT_ALL"))
        self.actionZOOM = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/zoom-in.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZOOM.setIcon(icon4)
        self.actionZOOM.setObjectName(_fromUtf8("actionZOOM"))
        self.actionSTOP_MOTOR = QtGui.QAction(MainWindow)
        self.actionSTOP_MOTOR.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/playMotor.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/playMotor.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/playMotor.png")), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        self.actionSTOP_MOTOR.setIcon(icon5)
        self.actionSTOP_MOTOR.setObjectName(_fromUtf8("actionSTOP_MOTOR"))
        self.actionSPEED_FIX = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/speed.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSPEED_FIX.setIcon(icon6)
        self.actionSPEED_FIX.setObjectName(_fromUtf8("actionSPEED_FIX"))
        self.actionSPEED_STEP = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/step.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSPEED_STEP.setIcon(icon7)
        self.actionSPEED_STEP.setObjectName(_fromUtf8("actionSPEED_STEP"))
        self.actionRAZ_PLOT = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8("reset.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRAZ_PLOT.setIcon(icon8)
        self.actionRAZ_PLOT.setObjectName(_fromUtf8("actionRAZ_PLOT"))
        self.actionINIT_MOTOR = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/toolbar/power_reset_1847.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionINIT_MOTOR.setIcon(icon9)
        self.actionINIT_MOTOR.setObjectName(_fromUtf8("actionINIT_MOTOR"))
        self.toolBar.addAction(self.actionSTOP_MOTOR)
        self.toolBar.addAction(self.actionSPEED_FIX)
        self.toolBar.addAction(self.actionSPEED_STEP)
        self.toolBar.addAction(self.actionSTART_ACQ)
        self.toolBar.addAction(self.actionSTOP_Plot)
        self.toolBar.addAction(self.actionRAZ_PLOT)
        self.toolBar.addAction(self.actionSave_File)
        self.toolBar.addAction(self.actionZOOM)
        self.toolBar.addAction(self.actionQUIT_ALL)
        self.toolBar.addAction(self.actionINIT_MOTOR)

        self.retranslateUi(MainWindow)
        self.tabWidgetIHM.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "VISCODAQ 2.0 OPGC SDT", None))
        self.tabWidgetIHM.setTabText(self.tabWidgetIHM.indexOf(self.tabAcquisition), _translate("MainWindow", "Data Acquisition and Control", None))
        self.checkBoxSpeed.setText(_translate("MainWindow", "speed", None))
        self.checkBoxTorque.setText(_translate("MainWindow", "torque", None))
        self.checkBoxTempC.setText(_translate("MainWindow", "tempC", None))
        self.pushButtonLoadData.setText(_translate("MainWindow", "LOAD", None))
        self.tabWidgetIHM.setTabText(self.tabWidgetIHM.indexOf(self.Look), _translate("MainWindow", "Look up Graph", None))
        item = self.tableWidgetData.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "date", None))
        item = self.tableWidgetData.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "time(s)", None))
        item = self.tableWidgetData.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "speed(tr/min)", None))
        item = self.tableWidgetData.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "torque(mN.m)", None))
        item = self.tableWidgetData.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "temp(°C)", None))
        self.tabWidgetIHM.setTabText(self.tabWidgetIHM.indexOf(self.tabLookup), _translate("MainWindow", "Look up Table", None))
        self.groupBoxCmdMotor.setTitle(_translate("MainWindow", "ACQUISITION  CONTROLS", None))
        self.radioButtonSpeed.setText(_translate("MainWindow", "Speed", None))
        self.label_3.setText(_translate("MainWindow", "Cursors select:", None))
        self.label_2.setText(_translate("MainWindow", "Threshold (mN.m):", None))
        self.radioButtonTorque.setText(_translate("MainWindow", "Torque", None))
        self.radioButtonTemperature.setText(_translate("MainWindow", "Temperature", None))
        self.label.setText(_translate("MainWindow", "Window time(s):", None))
        self.labelComPort.setText(_translate("MainWindow", "Com port:", None))
        self.toolButtonUpdateCom.setText(_translate("MainWindow", "Update Com", None))
        self.labelComPort_2.setText(_translate("MainWindow", "Gear reducer:", None))
        self.comboBoxGear.setItemText(0, _translate("MainWindow", "1/100", None))
        self.comboBoxGear.setItemText(1, _translate("MainWindow", "1/25", None))
        self.tabWidgetIHM.setTabText(self.tabWidgetIHM.indexOf(self.tabAnalysis), _translate("MainWindow", "Configurations", None))
        self.labelSpeed.setText(_translate("MainWindow", "N(tr/min):", None))
        self.labelTorque.setText(_translate("MainWindow", "T(mN.m):", None))
        self.labelTemperature.setText(_translate("MainWindow", "Temp(°C):", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionSTART_ACQ.setText(_translate("MainWindow", "START PLOT", None))
        self.actionSTART_ACQ.setToolTip(_translate("MainWindow", "Plotting data", None))
        self.actionSTOP_Plot.setText(_translate("MainWindow", "STOP PLOT", None))
        self.actionSave_File.setText(_translate("MainWindow", "SAVE FILE", None))
        self.actionSave_File.setToolTip(_translate("MainWindow", "Save data to file", None))
        self.actionQUIT_ALL.setText(_translate("MainWindow", "QUIT ALL", None))
        self.actionQUIT_ALL.setToolTip(_translate("MainWindow", "Close Software", None))
        self.actionZOOM.setText(_translate("MainWindow", "ZOOM", None))
        self.actionZOOM.setToolTip(_translate("MainWindow", "Enable/Disable zoom", None))
        self.actionSTOP_MOTOR.setText(_translate("MainWindow", "ON/OFF MOTOR", None))
        self.actionSTOP_MOTOR.setToolTip(_translate("MainWindow", "On/Off Motor", None))
        self.actionSPEED_FIX.setText(_translate("MainWindow", "SPEED FIX", None))
        self.actionSPEED_FIX.setToolTip(_translate("MainWindow", "Send a fix Speed to motor", None))
        self.actionSPEED_STEP.setText(_translate("MainWindow", "SPEED STEP", None))
        self.actionSPEED_STEP.setToolTip(_translate("MainWindow", "Send Step speed command to motor", None))
        self.actionRAZ_PLOT.setText(_translate("MainWindow", "RAZ PLOT", None))
        self.actionRAZ_PLOT.setToolTip(_translate("MainWindow", "reset all graph", None))
        self.actionINIT_MOTOR.setText(_translate("MainWindow", "INIT MOTOR", None))
        self.actionINIT_MOTOR.setToolTip(_translate("MainWindow", "Init motor position", None))

from PyQt4 import Qwt5
import ToolBarIcon_rc
