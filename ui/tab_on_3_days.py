# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\tab_on_3_days.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(610, 410)
        Form.setAutoFillBackground(True)
        self.lbl_day_1 = QtWidgets.QLabel(Form)
        self.lbl_day_1.setGeometry(QtCore.QRect(10, 20, 191, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_day_1.setFont(font)
        self.lbl_day_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_day_1.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_day_1.setObjectName("lbl_day_1")
        self.lbl_day_2 = QtWidgets.QLabel(Form)
        self.lbl_day_2.setGeometry(QtCore.QRect(210, 20, 191, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_day_2.setFont(font)
        self.lbl_day_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_day_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_day_2.setObjectName("lbl_day_2")
        self.lbl_day_3 = QtWidgets.QLabel(Form)
        self.lbl_day_3.setGeometry(QtCore.QRect(410, 20, 191, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_day_3.setFont(font)
        self.lbl_day_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lbl_day_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_day_3.setObjectName("lbl_day_3")
        self.lbl_morning_img_1 = QtWidgets.QLabel(Form)
        self.lbl_morning_img_1.setGeometry(QtCore.QRect(20, 460, 101, 21))
        self.lbl_morning_img_1.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_morning_img_1.setObjectName("lbl_morning_img_1")
        self.lbl_evening_img_1 = QtWidgets.QLabel(Form)
        self.lbl_evening_img_1.setGeometry(QtCore.QRect(20, 540, 101, 21))
        self.lbl_evening_img_1.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_evening_img_1.setObjectName("lbl_evening_img_1")
        self.lbl_day_img_1 = QtWidgets.QLabel(Form)
        self.lbl_day_img_1.setGeometry(QtCore.QRect(20, 500, 101, 21))
        self.lbl_day_img_1.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_day_img_1.setObjectName("lbl_day_img_1")
        self.lbl_morning_img_2 = QtWidgets.QLabel(Form)
        self.lbl_morning_img_2.setGeometry(QtCore.QRect(130, 460, 101, 21))
        self.lbl_morning_img_2.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_morning_img_2.setObjectName("lbl_morning_img_2")
        self.lbl_day_img_2 = QtWidgets.QLabel(Form)
        self.lbl_day_img_2.setGeometry(QtCore.QRect(130, 500, 101, 21))
        self.lbl_day_img_2.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_day_img_2.setObjectName("lbl_day_img_2")
        self.lbl_evening_img_2 = QtWidgets.QLabel(Form)
        self.lbl_evening_img_2.setGeometry(QtCore.QRect(130, 540, 101, 21))
        self.lbl_evening_img_2.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_evening_img_2.setObjectName("lbl_evening_img_2")
        self.lbl_morning_img_3 = QtWidgets.QLabel(Form)
        self.lbl_morning_img_3.setGeometry(QtCore.QRect(240, 460, 101, 21))
        self.lbl_morning_img_3.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_morning_img_3.setObjectName("lbl_morning_img_3")
        self.lbl_day_img_3 = QtWidgets.QLabel(Form)
        self.lbl_day_img_3.setGeometry(QtCore.QRect(240, 500, 101, 21))
        self.lbl_day_img_3.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_day_img_3.setObjectName("lbl_day_img_3")
        self.lbl_evening_img_3 = QtWidgets.QLabel(Form)
        self.lbl_evening_img_3.setGeometry(QtCore.QRect(240, 540, 101, 21))
        self.lbl_evening_img_3.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_evening_img_3.setObjectName("lbl_evening_img_3")
        self.lbl_clouds_img_1 = QtWidgets.QLabel(Form)
        self.lbl_clouds_img_1.setGeometry(QtCore.QRect(20, 570, 101, 21))
        self.lbl_clouds_img_1.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_clouds_img_1.setObjectName("lbl_clouds_img_1")
        self.lbl_clouds_img_2 = QtWidgets.QLabel(Form)
        self.lbl_clouds_img_2.setGeometry(QtCore.QRect(130, 570, 101, 21))
        self.lbl_clouds_img_2.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_clouds_img_2.setObjectName("lbl_clouds_img_2")
        self.lbl_clouds_img_3 = QtWidgets.QLabel(Form)
        self.lbl_clouds_img_3.setGeometry(QtCore.QRect(240, 570, 101, 21))
        self.lbl_clouds_img_3.setFrameShape(QtWidgets.QFrame.Box)
        self.lbl_clouds_img_3.setObjectName("lbl_clouds_img_3")
        self.lw_day_1 = QtWidgets.QListWidget(Form)
        self.lw_day_1.setGeometry(QtCore.QRect(10, 50, 191, 351))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_day_1.sizePolicy().hasHeightForWidth())
        self.lw_day_1.setSizePolicy(sizePolicy)
        self.lw_day_1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lw_day_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_day_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_day_1.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.lw_day_1.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lw_day_1.setObjectName("lw_day_1")
        self.lw_day_2 = QtWidgets.QListWidget(Form)
        self.lw_day_2.setGeometry(QtCore.QRect(210, 50, 191, 351))
        self.lw_day_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lw_day_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_day_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_day_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lw_day_2.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lw_day_2.setObjectName("lw_day_2")
        self.lw_day_3 = QtWidgets.QListWidget(Form)
        self.lw_day_3.setGeometry(QtCore.QRect(410, 50, 191, 351))
        self.lw_day_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lw_day_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_day_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.lw_day_3.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lw_day_3.setObjectName("lw_day_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_day_1.setText(_translate("Form", "ПН. 12.12.2020"))
        self.lbl_day_2.setText(_translate("Form", "ПН. 12.12.2020"))
        self.lbl_day_3.setText(_translate("Form", "ПН. 12.12.2020"))
        self.lbl_morning_img_1.setText(_translate("Form", "Утро"))
        self.lbl_evening_img_1.setText(_translate("Form", "Ночь"))
        self.lbl_day_img_1.setText(_translate("Form", "День"))
        self.lbl_morning_img_2.setText(_translate("Form", "Утро"))
        self.lbl_day_img_2.setText(_translate("Form", "День"))
        self.lbl_evening_img_2.setText(_translate("Form", "Ночь"))
        self.lbl_morning_img_3.setText(_translate("Form", "Утро"))
        self.lbl_day_img_3.setText(_translate("Form", "День"))
        self.lbl_evening_img_3.setText(_translate("Form", "Ночь"))
        self.lbl_clouds_img_1.setText(_translate("Form", "Облачность"))
        self.lbl_clouds_img_2.setText(_translate("Form", "Облачность"))
        self.lbl_clouds_img_3.setText(_translate("Form", "Облачность"))
        self.lw_day_1.setToolTip(_translate("Form", "Область скролируется"))
        self.lw_day_2.setToolTip(_translate("Form", "Область скролируется"))
        self.lw_day_3.setToolTip(_translate("Form", "Область скролируется"))
