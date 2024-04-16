import codecs
import configparser
import datetime
from email import message
import logging
import os
import subprocess
import threading
import xmlrpc.client
from time import sleep
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QWidget)
import paramiko



class ToolsUI(QDialog):
    def __init__(self):
        super(QDialog,self).__init__()
        self.setWindowIcon(QtGui.QIcon(r'ico\blizzard.ico'))
        
        self.getConfig()
        self.mainLayout = QVBoxLayout()   
        self.setMinimumSize(600,300)
        self.addWidget() 
        self.setLayout(self.mainLayout)
        self.setWindowTitle('辅助工具')
        
        # self.message = QtWidgets.QMessageBox()
    
    def getConfig(self):
        # 使用 codecs 打开文件，并指定编码  
        with codecs.open("Tools.ini", 'r', 'utf-8-sig') as file:  
            # codecs 的 'utf-8-sig' 会自动处理 BOM  
            content = file.read()
        self.config = configparser.ConfigParser()
        self.config.read_string(content)
        self.RemoteControlList = self.config.get("RemoteControl", "RemoteControlList").split(',')
        self.RemoteControlList = [name.strip() for name in self.RemoteControlList]
        self.RouterList = self.config.get("RouterReboot", "RouterList").split(',')
        self.RouterList = [name.strip() for name in self.RouterList]
        self.OSList = self.config.get("OSReboot", "OSList").split(',')
        self.OSList = [name.strip() for name in self.OSList]
        self.OtherList = self.config.get("Other", "OtherList").split(',')
        self.OtherList = [name.strip() for name in self.OtherList]

    
    #创建通用GroupBox及项目控件    
    def createGroupBox(self, groupBoxTite, groupBoxName, List):
        self.GridGroupBox = QGroupBox(groupBoxTite)
        layout = QGridLayout()

        for i in range(len(List)):
            button = QPushButton(List[i])
            button.setObjectName(groupBoxName + '_' + List[i])
            layout.addWidget(button,i//5, i%5)
            setattr(self, groupBoxName+List[i], button)
            button.clicked.connect(self.execute)

        self.GridGroupBox.setLayout(layout)
        self.mainLayout.addWidget(self.GridGroupBox)
     
     #根据配置文件动态生成相关控件   
    def addWidget(self):
        if len(self.RemoteControlList) > 0:
            self.createGroupBox('远程桌面控制', 'remoteControl', self.RemoteControlList)
        if len(self.RouterList) > 0:
            self.createGroupBox('流水线Router程序重启', 'routerReboot', self.RouterList)
        if len(self.OSList) > 0:
            self.createGroupBox('操作系统远程重启', 'OSReboot', self.OSList)
        if len(self.OtherList) > 0:
            self.createGroupBox('其它工具', 'other', self.OtherList)
            
        self.browser = QTextEdit()
        self.browser.setReadOnly(True)
        self.mainLayout.addWidget(self.browser)
    
    def execute(self):
        widgetName = self.sender().objectName()
        groupBox = widgetName.split('_', 1)[0]
        pbname = widgetName.split('_', 1)[1]
        print(groupBox)
        method = getattr(self, groupBox, None)
        method(pbname)
        
        
        
    #远程桌面控制
    def remoteControl(self, name):
        remoteControlPath = self.config.get('RemoteControl', name + '.RemoteControlPath').strip()
        VNCPath = self.config.get('RemoteControl', 'VNCPath').strip()
        RDPPath = self.config.get('RemoteControl', 'RDPPath').strip()
        
        # 检查文件是否存在  
        if os.path.exists(remoteControlPath): 
            if remoteControlPath.split('.')[-1] == 'rdp':
                # 使用mstsc.exe打开RDP文件  
                # 注意：这里假设mstsc.exe在系统的PATH环境变量中，通常这是默认的  
                subprocess.Popen([RDPPath, remoteControlPath])
            elif remoteControlPath.split('.')[-1] == 'vnc':
                subprocess.Popen([VNCPath, remoteControlPath])  
                # subprocess.Popen(['notepad.exe', remoteControlPath])
        else:  
            self.caution(f'文件 {remoteControlPath} 不存在!')
    
    #流水线Router程序重启
    def routerReboot(self, name):
        routerIp = self.config.get('RouterReboot', name + '.IP').strip()
        batPath = self.config.get('RouterReboot', 'batPath').strip()
        processName = self.config.get('RouterReboot', 'processName').strip()
        
        server_url = 'http://' + routerIp + ':18888'
        
        RouterThreading = threading.Thread(target=self.routerRebootThreading, args=(name, server_url, processName, batPath), daemon=True)
        RouterThreading.start()
        
    # 流水线Router程序重启功能具体实现，并提供给线程调用       
    def routerRebootThreading(self, name, server_url, processName, batPath):
        try:
            button = getattr(self,'routerReboot' + name, None)
            button.setDisabled(True)
            # 连接到XML-RPC服务器
            proxy = xmlrpc.client.ServerProxy(server_url)
            # 调用方法并获取结果
            result = proxy.rebootRouter(processName, batPath)
            if result:
                logging.debug(f"{name}主机Router程序已重启")
                #添加弹框提示
                self.caution(f"{name}主机Router程序已重启") 
            else:
                logging.debug(f"{name}主机Router程序重启失败")
                #添加弹框提示
                self.caution(f"{name}主机Router程序重启失败")
            button.setEnabled(True)
        except Exception as e:
            button.setEnabled(True)
            logging.warning(f"{name}主机XML-RPC服务连接异常" + str(e))
            #添加弹框提示
            self.caution(f'{name}主机XML-RPC服务连接异常')
        

    #操作系统远程重启
    def OSReboot(self, name):
        reply = QtWidgets.QMessageBox.question(self, '提示',
                                               "可能会影响流水线正常运行，确定重启？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            pass 
        else:
            return
        
        OSIp = self.config.get('OSReboot', name + '.IP').strip()
        
        RebootThreading = threading.Thread(target=self.OSRebootThreading, args=(name, OSIp), daemon=True)
        RebootThreading.start()
        
    #操作系统远程重启具体实现，并提供给线程调用           
    def OSRebootThreading(self, name, OSIp):
        button = getattr(self,'OSReboot' + name, None)
        button.setDisabled(True)
        if name == 'DMS':
            try:
                # 创建SSH客户端
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机名和主机密钥到本地HostKeys对象，并保存
                client.connect(OSIp, username='root', password='inpeco!it')
                # 执行netstat命令并获取输出
                stdin, stdout, stderr = client.exec_command("reboot")
                netstat_info = stdout.read().decode()
                # 关闭连接
                client.close()
                button.setEnabled(True)
                self.caution(f'{name}系统重启中')
                logging.debug(netstat_info)
            except:
                button.setEnabled(True)
                self.caution(f'执行{name}系统重启失败')
                logging.warning("OSRebootThreading()函数执行异常")     
        else:
            server_url = 'http://' + OSIp + ':18888'
            try:
                # 连接到XML-RPC服务器
                proxy = xmlrpc.client.ServerProxy(server_url)
                # 调用方法并获取结果
                result = proxy.rebootOS()
                if result:
                    self.caution(f'{name}系统重启中')
                else:
                    self.caution(f'执行{name}系统重启失败')
                    print(f'执行{name}系统重启失败')
                button.setEnabled(True)
            except:
                button.setEnabled(True)
                self.caution(f'{name}主机XML-RPC服务连接异常')
        
    
    #其它工具
    def other(self, name):
        print('other', name)
        
    #信息反馈弹框
    def caution(self, remider):
        # 获取当前时间
        currentTime = datetime.datetime.now()
        # 格式化时间
        formattedTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        self.browser.append(formattedTime + '  ' + remider +'\n')
            
        
        
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    dialog = ToolsUI()
    sys.exit(dialog.exec_())
        
        
        
    