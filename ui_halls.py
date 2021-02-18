# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_halls.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_H(object):
    def setupUi(self, Dialog_H):
        Dialog_H.setObjectName("Dialog_H")
        Dialog_H.resize(445, 290)
        Dialog_H.setMinimumSize(QtCore.QSize(445, 290))
        self.gridLayout = QtWidgets.QGridLayout(Dialog_H)
        self.gridLayout.setObjectName("gridLayout")
        self.halls_type = QtWidgets.QComboBox(Dialog_H)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.halls_type.setFont(font)
        self.halls_type.setObjectName("halls_type")
        self.gridLayout.addWidget(self.halls_type, 0, 0, 1, 1)
        self.info = QtWidgets.QLineEdit(Dialog_H)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.info.setFont(font)
        self.info.setObjectName("info")
        self.gridLayout.addWidget(self.info, 0, 1, 1, 1)
        self.table = QtWidgets.QTableWidget(Dialog_H)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.table.setFont(font)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 2)
        self.add_hall_btn = QtWidgets.QPushButton(Dialog_H)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.add_hall_btn.setFont(font)
        self.add_hall_btn.setObjectName("add_hall_btn")
        self.gridLayout.addWidget(self.add_hall_btn, 2, 0, 1, 2)

        self.retranslateUi(Dialog_H)
        QtCore.QMetaObject.connectSlotsByName(Dialog_H)

    def retranslateUi(self, Dialog_H):
        _translate = QtCore.QCoreApplication.translate
        Dialog_H.setWindowTitle(_translate("Dialog_H", "Залы"))
        self.info.setPlaceholderText(_translate("Dialog_H", "введите название зала"))
        self.add_hall_btn.setText(_translate("Dialog_H", "Добавить"))
