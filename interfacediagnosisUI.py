# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InterfaceDiagnosis.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from networkdiagnosis import networkdiagnosis


class interfacediagnosisUI(object):
    def __init__(self, networkdiagnosis):
        self.networkdiagnosis = networkdiagnosis
        # self.networkdiagnosis = networkdiagnosis()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1704, 877)
        Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 1691, 80))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 110, 1691, 751))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self._translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(self._translate("Dialog", "通讯端口诊断"))
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.addwidget()

        self.networkdiagnosis.interfacediagnosisstart(self, Dialog)

    # 动态添加控件
    def addwidget(self):
        for module in self.networkdiagnosis.modulelist:
            modulename = module.name
            # 添加上面控件
            if modulename.upper().find('DMS') + modulename.upper().find('ADM') + modulename.upper().find('CENTRALINK') \
                    + modulename.upper().find('DATALINK') + modulename.upper().find('LIS') == -5:
                widgetname = 'pbInstruments'
                instrumentname = 'Instruments'
            else:
                widgetname = 'pb' + modulename
                instrumentname = modulename
            if not getattr(self, widgetname, None):
                widget = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
                widget.setSizePolicy(sizePolicy)
                font = QtGui.QFont()
                font.setPointSize(13)
                widget.setFont(font)
                widget.setObjectName(widgetname)
                self.horizontalLayout_2.addWidget(widget)
                widget.setText(self._translate("Dialog", instrumentname))
                setattr(self, widgetname, widget)

            # 添加左边控件
            leftlist = self.networkdiagnosis.moduledict[modulename].interfaceleft
            if leftlist[0]:
                for leftitem in leftlist:
                    interfacename = leftitem.split(':')[0].strip()
                    self.addbutton(instrumentname, interfacename, 'left')
            elif instrumentname == 'Instruments':
                self.addbutton('Instruments', 'invisible', 'left')

            # 添加右边控件
            rightlist = self.networkdiagnosis.moduledict[modulename].interfaceright
            if rightlist[0]:
                for rightitem in rightlist:
                    interfacename = rightitem.split(':')[0].strip()
                    self.addbutton(instrumentname, interfacename, 'right')
            elif instrumentname == 'LIS':
                self.addbutton('LIS', 'invisible', 'right')

    def addbutton(self, modulename, interfacename, leftorright, ):
        vl = getattr(self, 'vl' + modulename + leftorright, None)
        if not vl:
            if leftorright == 'left':
                self.addline(modulename, leftorright)
            vl = QtWidgets.QVBoxLayout()
            vl.setObjectName(modulename + leftorright)
            setattr(self, 'vl' + modulename + leftorright, vl)
        else:
            if getattr(self, 'pb' + modulename + interfacename, None):
                return

        widget = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        widget.setMinimumSize(QtCore.QSize(0, 60))
        font = QtGui.QFont()
        font.setPointSize(8)
        widget.setFont(font)
        widget.setObjectName(modulename + interfacename)
        vl.addWidget(widget)
        self.horizontalLayout.addLayout(vl)
        widget.setText(self._translate("Dialog", interfacename))
        setattr(self, 'pb' + modulename + interfacename, widget)
        if interfacename == 'invisible':
            widget.setEnabled(False)
            widget.setText(self._translate("Dialog", ''))
            widget.setMinimumSize(QtCore.QSize(0, 1))

        if leftorright == 'right' and modulename == 'LIS':
            self.addline(modulename, leftorright)

    # 加一根分割线
    def addline(self, modulename, leftorright):
        self.line = QtWidgets.QFrame(self.horizontalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName(modulename + leftorright)
        self.horizontalLayout.addWidget(self.line)


# 创建一个QDialog子类
class CustominterfaceDialog(QtWidgets.QDialog):
    def closeEvent(self, event):
        # 阻止对话框被关闭，但隐藏它
        event.ignore()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    m = interfacediagnosisUI()
    m.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())
