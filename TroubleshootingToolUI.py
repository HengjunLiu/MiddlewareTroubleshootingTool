# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MiddlewareTroubleshootingTool.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


class base_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(1126, 648)
        self.horizontalLayoutWidget = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 1091, 91))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pbPortDiagnose = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbPortDiagnose.sizePolicy().hasHeightForWidth())
        self.pbPortDiagnose.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pbPortDiagnose.setFont(font)
        self.pbPortDiagnose.setObjectName("pbPortDiagnose")
        self.horizontalLayout.addWidget(self.pbPortDiagnose)
        self.pbLogAnalysis = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbLogAnalysis.sizePolicy().hasHeightForWidth())
        self.pbLogAnalysis.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pbLogAnalysis.setFont(font)
        self.pbLogAnalysis.setObjectName("pbLogAnalysis")
        self.horizontalLayout.addWidget(self.pbLogAnalysis)
        
        self.pbAuxiliaryTool = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pbAuxiliaryTool.sizePolicy().hasHeightForWidth())
        self.pbAuxiliaryTool.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pbAuxiliaryTool.setFont(font)
        self.pbAuxiliaryTool.setObjectName("pbAuxiliaryTool")
        self.horizontalLayout.addWidget(self.pbAuxiliaryTool)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 130, 1091, 471))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(dialog)


    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "通讯诊断工具"))
        self.pbPortDiagnose.setText(_translate("dialog", "通讯端口诊断"))
        self.pbLogAnalysis.setText(_translate("dialog", "通讯日志分析"))
        self.pbAuxiliaryTool.setText(_translate("dialog", "辅助工具"))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    m = base_dialog()
    m.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())