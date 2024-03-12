import sys
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

from TroubleshootingToolUI import base_dialog
from networkdiagnosis import networkdiagnosis
from interfacediagnosisUI import interfacediagnosisUI, CustominterfaceDialog

logging.basicConfig(level=logging.DEBUG,  
                    format='%(asctime)s - %(levelname)s - %(message)s',  
                    filename='debug.log',  # 日志文件名，如果没有这个参数，日志输出到console  
                    filemode='w')  # 文件写入模式，“w”会覆盖之前的日志，“a”会追加到之前的日志 


class main(base_dialog):
    def __init__(self):
        self.ui = None
        pass

    def setupUi(self, dialog):
        super(main, self).setupUi(dialog)
        dialog.setWindowFlags(dialog.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)
        self.networkdiag = networkdiagnosis()
        self.networkdiag.networkdiagnosisstart(self, dialog)

        self.pbPortDiagnose.clicked.connect(self.openinterfacediagnosisUI)
        # modulelist = ["ChemstryXPT-1", "CentaurXPT-1", "Atellica", "TerminalServer", "immunite2000", "Aptio", "DMS", "ADM", "DataLink", "LIS"]
        # 根据配置文件中的设备列表，实时添加对应控件
        self.addwidget(self.networkdiag.modulenamelist)
        # 添加系统托盘图标
        self.systemTrayIcon = SystemTrayIcon(dialog)
        self.systemTrayIcon.show()

    # 打开通讯接口监控界面
    def openinterfacediagnosisUI(self):
        if not self.ui:
            self.dialogII = CustominterfaceDialog()
            self.ui = interfacediagnosisUI(self.networkdiag)
            self.ui.setupUi(self.dialogII)
            self.dialogII.show()
        else:
            self.dialogII.show()

    # 动态添加控件
    def addwidget(self, modulenamelist):
        for modulename in modulenamelist:
            widgetname = 'pb' + modulename
            widget = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
            widget.setSizePolicy(sizePolicy)
            font = QtGui.QFont()
            font.setPointSize(12)
            widget.setFont(font)
            widget.setObjectName(widgetname)

            if modulename.upper() not in ['ATM', 'DMS', 'ADM', 'CENTRALINK', 'DATALINK', 'LIS']:
                self.verticalLayout.addWidget(widget)
            else:
                font.setPointSize(16)
                self.horizontalLayout_2.addWidget(widget)
            _translate = QtCore.QCoreApplication.translate
            widget.setText(_translate("dialog", modulename))
            setattr(self, widgetname, widget)
            # 触发点击事件
            widget.clicked.connect(getattr(self.networkdiag.moduledict[modulename], 'checknetworkconnectionSOP'))
            # print('addwidget', modulename)


# 这是一个托盘类，后期还需要进行功能拓展
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, parent=None):
        self.parent = parent
        icon = QtGui.QIcon('TrayIcon.ico')
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtWidgets.QMenu(parent)
        self.exitAction = self.menu.addAction("Exit")
        self.exitAction.triggered.connect(self.close)
        self.setContextMenu(self.menu)
        self.activated.connect(self.onTrayIconActivated)  # 连接信号和槽

    def onTrayIconActivated(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:  # 判断双击事件
            self.parent.showNormal()  # 显示窗口
            self.parent.raise_()  # 提升窗口到其他窗口的前面

    def close(self):
        QtWidgets.QApplication.quit()


# 创建一个QDialog子类
class CustomDialog(QtWidgets.QDialog):
    def closeEvent(self, event):
        # 创建确认框
        reply = QtWidgets.QMessageBox.question(self, '提示',
                                               "确定退出程序?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()  # 接受关闭事件
        else:
            event.ignore()  # 忽略关闭事件


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = CustomDialog()
    m = main()
    m.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())
