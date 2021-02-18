# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_enter.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_L(object):
    def setupUi(self, Dialog_L):
        Dialog_L.setObjectName("Dialog_L")
        Dialog_L.resize(325, 150)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_L.sizePolicy().hasHeightForWidth())
        Dialog_L.setSizePolicy(sizePolicy)
        Dialog_L.setMinimumSize(QtCore.QSize(325, 150))
        Dialog_L.setMaximumSize(QtCore.QSize(325, 150))
        self.gridLayout = QtWidgets.QGridLayout(Dialog_L)
        self.gridLayout.setObjectName("gridLayout")
        self.log = QtWidgets.QLabel(Dialog_L)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.log.setFont(font)
        self.log.setObjectName("log")
        self.gridLayout.addWidget(self.log, 0, 0, 1, 1)
        self.log_ent = QtWidgets.QLineEdit(Dialog_L)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_ent.sizePolicy().hasHeightForWidth())
        self.log_ent.setSizePolicy(sizePolicy)
        self.log_ent.setObjectName("log_ent")
        self.gridLayout.addWidget(self.log_ent, 0, 1, 1, 1)
        self.password = QtWidgets.QLabel(Dialog_L)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.password.setFont(font)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 1, 0, 1, 1)
        self.password_ent = QtWidgets.QLineEdit(Dialog_L)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_ent.sizePolicy().hasHeightForWidth())
        self.password_ent.setSizePolicy(sizePolicy)
        self.password_ent.setObjectName("password_ent")
        self.gridLayout.addWidget(self.password_ent, 1, 1, 1, 1)
        self.ok = QtWidgets.QPushButton(Dialog_L)
        self.ok.setObjectName("ok")
        self.gridLayout.addWidget(self.ok, 2, 0, 1, 1)
        self.cancel = QtWidgets.QPushButton(Dialog_L)
        self.cancel.setObjectName("cancel")
        self.gridLayout.addWidget(self.cancel, 2, 1, 1, 1)

        self.retranslateUi(Dialog_L)
        QtCore.QMetaObject.connectSlotsByName(Dialog_L)

    def retranslateUi(self, Dialog_L):
        _translate = QtCore.QCoreApplication.translate
        Dialog_L.setWindowTitle(_translate("Dialog_L", "Вход"))
        self.log.setText(_translate("Dialog_L", "Введите логин:"))
        self.password.setText(_translate("Dialog_L", "Введите пароль:"))
        self.ok.setText(_translate("Dialog_L", "OK"))
        self.cancel.setText(_translate("Dialog_L", "Отмена"))
        self.cancel.setShortcut(_translate("Dialog_L", "Esc"))
