# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(287, 322)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelStep = QtGui.QLabel(Dialog)
        self.labelStep.setObjectName(_fromUtf8("labelStep"))
        self.gridLayout.addWidget(self.labelStep, 1, 1, 1, 1)
        self.SpinBoxStep = QtGui.QSpinBox(Dialog)
        self.SpinBoxStep.setObjectName(_fromUtf8("SpinBoxStep"))
        self.gridLayout.addWidget(self.SpinBoxStep, 1, 2, 1, 1)
        self.tableWidgetStep = QtGui.QTableWidget(Dialog)
        self.tableWidgetStep.setColumnCount(2)
        self.tableWidgetStep.setObjectName(_fromUtf8("tableWidgetStep"))
        self.tableWidgetStep.setRowCount(0)
        self.tableWidgetStep.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetStep.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidgetStep.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.tableWidgetStep, 5, 1, 1, 3)
        self.pushButtonOpenfile = QtGui.QPushButton(Dialog)
        self.pushButtonOpenfile.setObjectName(_fromUtf8("pushButtonOpenfile"))
        self.gridLayout.addWidget(self.pushButtonOpenfile, 6, 2, 1, 1)
        self.pushButtonSavefile = QtGui.QPushButton(Dialog)
        self.pushButtonSavefile.setObjectName(_fromUtf8("pushButtonSavefile"))
        self.gridLayout.addWidget(self.pushButtonSavefile, 6, 3, 1, 1)
        self.pushButtonOK = QtGui.QPushButton(Dialog)
        self.pushButtonOK.setObjectName(_fromUtf8("pushButtonOK"))
        self.gridLayout.addWidget(self.pushButtonOK, 6, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.labelStep.setText(_translate("Dialog", "Number of Step:", None))
        self.tableWidgetStep.setSortingEnabled(False)
        self.pushButtonOpenfile.setText(_translate("Dialog", "Open file", None))
        self.pushButtonSavefile.setText(_translate("Dialog", "Save to file", None))
        self.pushButtonOK.setText(_translate("Dialog", "Ok", None))

