# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'walker.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126, 937)
        MainWindow.setMaximumSize(QtCore.QSize(1920, 1541))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainBox = QtWidgets.QVBoxLayout()
        self.mainBox.setContentsMargins(30, 30, 30, 30)
        self.mainBox.setObjectName("mainBox")
        self.topBox = QtWidgets.QHBoxLayout()
        self.topBox.setObjectName("topBox")
        self.view1 = QtWidgets.QScrollArea(self.centralwidget)
        self.view1.setMinimumSize(QtCore.QSize(350, 350))
        self.view1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.view1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.view1.setWidgetResizable(True)
        self.view1.setObjectName("view1")
        self.viewForm1 = QtWidgets.QWidget()
        self.viewForm1.setGeometry(QtCore.QRect(0, 0, 460, 409))
        self.viewForm1.setMinimumSize(QtCore.QSize(0, 0))
        self.viewForm1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.viewForm1.setObjectName("viewForm1")
        self.viewData1 = QtWidgets.QLabel(self.viewForm1)
        self.viewData1.setGeometry(QtCore.QRect(0, 0, 448, 349))
        self.viewData1.setMinimumSize(QtCore.QSize(320, 320))
        self.viewData1.setText("")
        self.viewData1.setObjectName("viewData1")
        self.view1.setWidget(self.viewForm1)
        self.topBox.addWidget(self.view1)
        self.view2 = QtWidgets.QScrollArea(self.centralwidget)
        self.view2.setMinimumSize(QtCore.QSize(350, 350))
        self.view2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.view2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.view2.setWidgetResizable(True)
        self.view2.setObjectName("view2")
        self.viewForm2 = QtWidgets.QWidget()
        self.viewForm2.setGeometry(QtCore.QRect(0, 0, 460, 409))
        self.viewForm2.setMinimumSize(QtCore.QSize(0, 0))
        self.viewForm2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.viewForm2.setObjectName("viewForm2")
        self.viewData2 = QtWidgets.QLabel(self.viewForm2)
        self.viewData2.setGeometry(QtCore.QRect(0, 0, 447, 349))
        self.viewData2.setMinimumSize(QtCore.QSize(320, 320))
        self.viewData2.setText("")
        self.viewData2.setObjectName("viewData2")
        self.view2.setWidget(self.viewForm2)
        self.topBox.addWidget(self.view2)
        self.mainBox.addLayout(self.topBox)
        self.midBox = QtWidgets.QHBoxLayout()
        self.midBox.setContentsMargins(0, 0, 0, 0)
        self.midBox.setObjectName("midBox")
        self.view3 = QtWidgets.QScrollArea(self.centralwidget)
        self.view3.setMinimumSize(QtCore.QSize(350, 350))
        self.view3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.view3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.view3.setWidgetResizable(True)
        self.view3.setObjectName("view3")
        self.viewForm3 = QtWidgets.QWidget()
        self.viewForm3.setGeometry(QtCore.QRect(0, 0, 460, 409))
        self.viewForm3.setMinimumSize(QtCore.QSize(0, 0))
        self.viewForm3.setObjectName("viewForm3")
        self.viewData3 = QtWidgets.QLabel(self.viewForm3)
        self.viewData3.setGeometry(QtCore.QRect(0, 0, 448, 349))
        self.viewData3.setMinimumSize(QtCore.QSize(320, 320))
        self.viewData3.setText("")
        self.viewData3.setObjectName("viewData3")
        self.view3.setWidget(self.viewForm3)
        self.midBox.addWidget(self.view3)
        self.view4 = QtWidgets.QScrollArea(self.centralwidget)
        self.view4.setMinimumSize(QtCore.QSize(350, 350))
        self.view4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.view4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.view4.setWidgetResizable(True)
        self.view4.setObjectName("view4")
        self.viewForm4 = QtWidgets.QWidget()
        self.viewForm4.setGeometry(QtCore.QRect(0, 0, 460, 409))
        self.viewForm4.setMinimumSize(QtCore.QSize(0, 0))
        self.viewForm4.setObjectName("viewForm4")
        self.viewData4 = QtWidgets.QLabel(self.viewForm4)
        self.viewData4.setGeometry(QtCore.QRect(0, 0, 447, 345))
        self.viewData4.setMinimumSize(QtCore.QSize(320, 320))
        self.viewData4.setText("")
        self.viewData4.setObjectName("viewData4")
        self.view4.setWidget(self.viewForm4)
        self.midBox.addWidget(self.view4)
        self.mainBox.addLayout(self.midBox)
        self.horizontalLayout.addLayout(self.mainBox)
        self.controlBox = QtWidgets.QVBoxLayout()
        self.controlBox.setContentsMargins(0, -1, -1, -1)
        self.controlBox.setObjectName("controlBox")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlBox.addItem(spacerItem)
        self.camBtn_auto = QtWidgets.QPushButton(self.centralwidget)
        self.camBtn_auto.setMinimumSize(QtCore.QSize(100, 40))
        self.camBtn_auto.setObjectName("camBtn_auto")
        self.controlBox.addWidget(self.camBtn_auto)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.controlBox.addItem(spacerItem1)
        self.camBtn_manual = QtWidgets.QPushButton(self.centralwidget)
        self.camBtn_manual.setMinimumSize(QtCore.QSize(100, 40))
        self.camBtn_manual.setObjectName("camBtn_manual")
        self.controlBox.addWidget(self.camBtn_manual)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.controlBox.addItem(spacerItem2)
        self.camBtn_save = QtWidgets.QPushButton(self.centralwidget)
        self.camBtn_save.setMinimumSize(QtCore.QSize(100, 40))
        self.camBtn_save.setObjectName("camBtn_save")
        self.controlBox.addWidget(self.camBtn_save)
        spacerItem3 = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlBox.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.controlBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Walker Webcam"))
        self.camBtn_auto.setText(_translate("MainWindow", "自動"))
        self.camBtn_manual.setText(_translate("MainWindow", "手動"))
        self.camBtn_save.setText(_translate("MainWindow", "存圖"))