# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_addfilm.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_AF(object):
    def setupUi(self, Dialog_AF):
        Dialog_AF.setObjectName("Dialog_AF")
        Dialog_AF.resize(260, 250)
        Dialog_AF.setMinimumSize(QtCore.QSize(260, 250))
        Dialog_AF.setMaximumSize(QtCore.QSize(260, 250))
        self.title = QtWidgets.QLineEdit(Dialog_AF)
        self.title.setGeometry(QtCore.QRect(100, 10, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.label = QtWidgets.QLabel(Dialog_AF)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog_AF)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog_AF)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog_AF)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 171, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.year = QtWidgets.QLineEdit(Dialog_AF)
        self.year.setGeometry(QtCore.QRect(50, 60, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.year.setFont(font)
        self.year.setMaxLength(4)
        self.year.setObjectName("year")
        self.dur = QtWidgets.QLineEdit(Dialog_AF)
        self.dur.setGeometry(QtCore.QRect(190, 160, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.dur.setFont(font)
        self.dur.setObjectName("dur")
        self.btn = QtWidgets.QPushButton(Dialog_AF)
        self.btn.setGeometry(QtCore.QRect(10, 200, 241, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btn.setFont(font)
        self.btn.setObjectName("btn")
        self.genre = QtWidgets.QComboBox(Dialog_AF)
        self.genre.setGeometry(QtCore.QRect(70, 111, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.genre.setFont(font)
        self.genre.setObjectName("genre")

        self.retranslateUi(Dialog_AF)
        QtCore.QMetaObject.connectSlotsByName(Dialog_AF)

    def retranslateUi(self, Dialog_AF):
        _translate = QtCore.QCoreApplication.translate
        Dialog_AF.setWindowTitle(_translate("Dialog_AF", "Добавить фильм"))
        self.label.setText(_translate("Dialog_AF", "Название"))
        self.label_2.setText(_translate("Dialog_AF", "Год"))
        self.label_3.setText(_translate("Dialog_AF", "Жанр"))
        self.label_4.setText(_translate("Dialog_AF", "Длительность, мин"))
        self.btn.setText(_translate("Dialog_AF", "Добавить"))
