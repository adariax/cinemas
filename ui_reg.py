# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_reg.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_R(object):
    def setupUi(self, Dialog_R):
        Dialog_R.setObjectName("Dialog_R")
        Dialog_R.resize(325, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog_R.sizePolicy().hasHeightForWidth())
        Dialog_R.setSizePolicy(sizePolicy)
        Dialog_R.setMinimumSize(QtCore.QSize(325, 200))
        Dialog_R.setMaximumSize(QtCore.QSize(325, 200))
        self.gridLayout = QtWidgets.QGridLayout(Dialog_R)
        self.gridLayout.setObjectName("gridLayout")
        self.log = QtWidgets.QLabel(Dialog_R)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.log.setFont(font)
        self.log.setObjectName("log")
        self.gridLayout.addWidget(self.log, 0, 0, 1, 1)
        self.log_ent = QtWidgets.QLineEdit(Dialog_R)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_ent.sizePolicy().hasHeightForWidth())
        self.log_ent.setSizePolicy(sizePolicy)
        self.log_ent.setObjectName("log_ent")
        self.gridLayout.addWidget(self.log_ent, 0, 1, 1, 1)
        self.name = QtWidgets.QLabel(Dialog_R)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 1, 0, 1, 1)
        self.name_ent = QtWidgets.QLineEdit(Dialog_R)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_ent.sizePolicy().hasHeightForWidth())
        self.name_ent.setSizePolicy(sizePolicy)
        self.name_ent.setObjectName("name_ent")
        self.gridLayout.addWidget(self.name_ent, 1, 1, 1, 1)
        self.password = QtWidgets.QLabel(Dialog_R)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.password.setFont(font)
        self.password.setObjectName("password")
        self.gridLayout.addWidget(self.password, 2, 0, 1, 1)
        self.password_ent = QtWidgets.QLineEdit(Dialog_R)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.password_ent.sizePolicy().hasHeightForWidth())
        self.password_ent.setSizePolicy(sizePolicy)
        self.password_ent.setObjectName("password_ent")
        self.gridLayout.addWidget(self.password_ent, 2, 1, 1, 1)
        self.ok = QtWidgets.QPushButton(Dialog_R)
        self.ok.setObjectName("ok")
        self.gridLayout.addWidget(self.ok, 3, 0, 1, 1)
        self.cancel = QtWidgets.QPushButton(Dialog_R)
        self.cancel.setObjectName("cancel")
        self.gridLayout.addWidget(self.cancel, 3, 1, 1, 1)

        self.retranslateUi(Dialog_R)
        QtCore.QMetaObject.connectSlotsByName(Dialog_R)

    def retranslateUi(self, Dialog_R):
        _translate = QtCore.QCoreApplication.translate
        Dialog_R.setWindowTitle(_translate("Dialog_R", "Регистрация"))
        self.log.setText(_translate("Dialog_R", "Введите логин:"))
        self.name.setText(_translate("Dialog_R", "Введите имя:"))
        self.password.setText(_translate("Dialog_R", "Введите пароль:"))
        self.ok.setText(_translate("Dialog_R", "OK"))
        self.ok.setShortcut(_translate("Dialog_R", "Return"))
        self.cancel.setText(_translate("Dialog_R", "Отмена"))
        self.cancel.setShortcut(_translate("Dialog_R", "Esc"))
