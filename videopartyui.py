# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'videopartyui.ui'
#
# Created: Mon Dec 28 12:19:31 2015
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
        MainWindow.resize(1099, 540)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(30, 30, 511, 421))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 91, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.tableView_2 = QtGui.QTableView(self.centralwidget)
        self.tableView_2.setGeometry(QtCore.QRect(560, 30, 521, 391))
        self.tableView_2.setObjectName(_fromUtf8("tableView_2"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(560, 430, 121, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(560, 10, 64, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(560, 450, 94, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(980, 450, 93, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1099, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Clip_Database = QtGui.QAction(MainWindow)
        self.actionOpen_Clip_Database.setObjectName(_fromUtf8("actionOpen_Clip_Database"))
        self.actionNew_Clip_Database = QtGui.QAction(MainWindow)
        self.actionNew_Clip_Database.setObjectName(_fromUtf8("actionNew_Clip_Database"))
        self.actionOpen_Media_File = QtGui.QAction(MainWindow)
        self.actionOpen_Media_File.setObjectName(_fromUtf8("actionOpen_Media_File"))
        self.menuFile.addAction(self.actionNew_Clip_Database)
        self.menuFile.addAction(self.actionOpen_Clip_Database)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_Media_File)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Clip Library", None))
        self.label_2.setText(_translate("MainWindow", "Total Duration:", None))
        self.label_3.setText(_translate("MainWindow", "Playlist", None))
        self.checkBox.setText(_translate("MainWindow", "Showtime", None))
        self.pushButton.setText(_translate("MainWindow", "Play", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionOpen_Clip_Database.setText(_translate("MainWindow", "Open Clip Database", None))
        self.actionNew_Clip_Database.setText(_translate("MainWindow", "New Clip Database", None))
        self.actionOpen_Media_File.setText(_translate("MainWindow", "Open Media File", None))

