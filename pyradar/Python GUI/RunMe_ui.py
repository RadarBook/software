# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RunMe.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(720, 555)
        font = QtGui.QFont()
        font.setPointSize(16)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Chapter02/python_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.toolsTree = QtWidgets.QTreeWidget(self.centralwidget)
        self.toolsTree.setGeometry(QtCore.QRect(310, 11, 256, 481))
        self.toolsTree.setObjectName("toolsTree")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.toolsTree.headerItem().setFont(0, font)
        item_0 = QtWidgets.QTreeWidgetItem(self.toolsTree)
        item_0 = QtWidgets.QTreeWidgetItem(self.toolsTree)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 720, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Introduction to Radar"))
        self.toolsTree.headerItem().setText(0, _translate("MainWindow", "Examples"))
        __sortingEnabled = self.toolsTree.isSortingEnabled()
        self.toolsTree.setSortingEnabled(False)
        self.toolsTree.topLevelItem(0).setText(0, _translate("MainWindow", "loop_gain"))
        self.toolsTree.topLevelItem(1).setText(0, _translate("MainWindow", "antenna"))
        self.toolsTree.setSortingEnabled(__sortingEnabled)

