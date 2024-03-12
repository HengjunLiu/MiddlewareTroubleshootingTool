import codecs
import configparser
import subprocess
import threading
import asyncio
import time,datetime
import xmlrpc.client
import logging

import paramiko
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMessageBox


class module:
    def __init__(self, dialog):
        self.dialog = dialog
        self.name = None
        self.ip = '6.6.6.6'
        self.ipII = None   #主要用在Datalink上，DL上除了Aptio内网IP,还有个跟LIS连接的IP
        self.netsolution = None
        self.networkconnected = None

        self.interfaceleft = []
        self.interfaceright = []

    async def isnetworkconnected(self):
        """网络是否连通"""
        ping_cmd = f'ping -n 1 {self.ip}'
        process = await asyncio.create_subprocess_shell(
            ping_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        # # 等待进程完成并获取输出
        stdout, stderr = await process.communicate()
        output = stdout.decode('utf-8', errors='ignore').strip()
        # 在返回值中找规律(中英文系统返回值不一样)
        if 'ms TTL=' in output:
            # print(f"{self.ip} is reachable",str(datetime.datetime.now().time()))
            logging.debug(f'{self.ip} is reachable')
            return True
        else:
            # print(f"{self.ip} is unreachable",str(datetime.datetime.now().time()))
            logging.debug(f"{self.ip} is unreachable")
            return False


    def checknetworkconnectionSOP(self):
        """返回处理网络连接的指导方法，纯文本信息，可从配置文件中提取"""
        if self.networkconnected:
            self.netsolution = '网络正常连接！'
        else:
            self.netsolution = self.netsolution.replace('\\', '').strip()
        msgBox = QMessageBox(self.dialog)
        font = QFont("Arial", 12)
        msgBox.setFont(font)
        msgBox.setWindowTitle('故障排查')
        msgBox.setText(self.netsolution)
        msgBox.exec_()

    #获取设备netstat信息
    def getnetstatinfo(self):
        server_url = 'http://' + self.ip.strip() +':18888'
        try:
            # 连接到XML-RPC服务器
            # server_url = "http://localhost:18888"
            proxy = xmlrpc.client.ServerProxy(server_url)
            # 调用方法并获取结果
            result = proxy.get_netstat_info()
        except Exception as e:
            # print(e)
            logging.warning(f"getnetstatinfo()执行异常" + str(e))
            result = ''
        return result

    def isipreachable(self, ipaddress):
        server_url = 'http://' + self.ip.strip() + ':18888'
        try:
            # 连接到XML-RPC服务器
            # server_url = "http://localhost:18888"
            proxy = xmlrpc.client.ServerProxy(server_url)
            # 调用方法并获取结果
            result = proxy.is_ip_reachable(ipaddress)
            # 在返回值中找规律(中英文系统返回值不一样)
            if 'ms TTL=' in result:
                # print(f"{ipaddress} is reachable",str(datetime.datetime.now().time()))
                logging.debug(f"{ipaddress} is reachable")
                return True
            else:
                # print(f"{ipaddress} is unreachable",str(datetime.datetime.now().time()))
                logging.debug(f"{ipaddress} is unreachable")
                return False
        except Exception as e:
            # print(e)
            logging.warning("isipreachable()执行异常" + str(e))
            return False


    def get_linux_netstat_info(self, ip):
        try:
            # 创建SSH客户端
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机名和主机密钥到本地HostKeys对象，并保存
            client.connect(ip, username='root', password='inpeco!it')
            # 执行netstat命令并获取输出
            stdin, stdout, stderr = client.exec_command("netstat -an | grep tcp")
            netstat_info = stdout.read().decode()
            # 关闭连接
            client.close()
            return netstat_info
        except:
            logging.warning("get_linux_netstat_info()函数执行异常")
            return ''
        

    def checkinterfacestatus(self):
        interfacestatus = {}
        interfacelist = self.interfaceleft + self.interfaceright
        if self.name.upper() == 'DMS':
            netstatinfo = self.get_linux_netstat_info(self.ip)
        elif self.name.upper() in ['ATM','ADM','CENTRALINK','DATALINK']:
            netstatinfo = self.getnetstatinfo()
        else:   #Instrument和LIS电脑无法直接检测端口状态，暂时不做处理
            netstatinfo = 'nothing'
        if netstatinfo:
            if self.name.upper() not in ['ATM', 'DMS', 'ADM', 'CENTRALINK', 'DATALINK', 'LIS']:
                modulename = 'Instruments'
            else:
                modulename = self.name
            for interfaceitem in interfacelist:
                if interfaceitem:
                    interfacename, interfaceip, interfaceport = interfaceitem.split(':')
                    if netstatinfo.find(interfaceip.strip() + ':' + interfaceport.strip()) > -1:
                        interfacestatus[modulename + interfacename] = 'ESTABLISHED'
                    elif interfaceip == self.ip or interfaceip == self.ipII:
                        if netstatinfo.find('0.0.0.0:' + interfaceport.strip()) > -1:
                            interfacestatus[modulename + interfacename.strip()] = 'LISTENING'
                        else:
                            interfacestatus[modulename + interfacename.strip()] = 'DISCONNECTED'
                    else:
                        interfacestatus[modulename + interfacename.strip()] = 'DISCONNECTED'
        return interfacestatus



class networkdiagnosis:
    def __init__(self):
        self.dialog = None
        self.main_UI = None

        self.dialogII = None
        self.interfaceUI = None
        self.allinterfacestatus ={}
        # 读取配置文件的模块信息
        # 使用 codecs 打开文件，并指定编码  
        with codecs.open("Configuration.ini", 'r', 'utf-8-sig') as file:  
            # codecs 的 'utf-8-sig' 会自动处理 BOM  
            content = file.read()
        self.config = configparser.ConfigParser()
        self.config.read_string(content)
        self.modulenamelist = self.config.get("ModuleNames", "NameList").split(',')
        # 清除设备名称前后可能存在的空格字符，并返回有效模块名称列表（供UI动态生成模块控件调用）
        self.modulenamelist = [name.strip() for name in self.modulenamelist]

        self.modulelist = []        #设备先后顺序有要求，所以用列表记录
        self.moduledict = {}        #在UI点击事件中，需要通过名字来找到对应的模块实例，所以用到字典记录
        self.addmodule()


    def addmodule(self):
        """根据配置文件添加各模块实例"""
        try:
            for name in self.modulenamelist:
                moduleobject = module(self.dialog)
                moduleobject.name = name
                iplist = self.config.get(name, 'IP').split(',')
                moduleobject.ip = iplist[0].strip()
                if len(iplist) > 1:
                    moduleobject.ipII = self.config.get(name, 'IP').split(',')[1].strip()
                moduleobject.netsolution = self.config.get(name,'netsolution').strip()
                moduleobject.interfaceleft = self.config.get(name, 'interfaces_left').split(',')
                moduleobject.interfaceleft = [lists.strip() for lists in moduleobject.interfaceleft]
                moduleobject.interfaceright = self.config.get(name, 'interfaces_right').split(',')
                moduleobject.interfaceright = [lists.strip() for lists in moduleobject.interfaceright]

                self.modulelist.append(moduleobject)
                self.moduledict[name] = moduleobject
        except:
            logging.critical(f"addmodule()-->{name}模块添加异常")



    def informUI(self,UI, modulename, status):
        """通知UI方法，将通讯故障模块控件背景色变成红色"""
        pushbutton = getattr(UI,'pb' + modulename, None)
        if pushbutton:
            if status == True or status == 'ESTABLISHED':
                pushbutton.setStyleSheet("QPushButton { background-color: #00FF00; }")   # 设置背景色为绿色
            elif status == 'LISTENING':
                pushbutton.setStyleSheet("QPushButton { background-color: #ffff00; }")  # 设置背景色为黄色
            elif status == 'DISCONNECTED':
                pushbutton.setStyleSheet("QPushButton { background-color: #FF0000; }")  # 设置背景色为红色
            else:
                pushbutton.setStyleSheet("QPushButton { background-color: #FF0000; }")  # 设置背景色为红色
                UI.systemTrayIcon.showMessage("提示", modulename + "网络故障")


    async def detectnetworkall(self):
        """监测每个模块网络连接情况，状态有变化就调用‘informUI()’"""
        list = [module.isnetworkconnected() for module in self.modulelist]
        results = await asyncio.gather(*list)
        for result, module in zip(results, self.modulelist):

            if module.name.upper() == 'LIS' and not result:
                for moduleI in self.modulelist:
                    if moduleI.name.upper() in ['ADM','CENTRALINK','DATALINK'] and moduleI.ipII:
                        result = moduleI.isipreachable(module.ip)
                        if result:
                            break
            if module.networkconnected != result or module.networkconnected is None:
                module.networkconnected = result
                self.informUI(self.main_UI, module.name, result)


    def detectallnetworkforever(self):
        """持续监控网络连接情况"""
        while True:
            try:
                asyncio.run(self.detectnetworkall())
                time.sleep(3)
            except:
                # print('detectallnetworkforever函数报错了！')
                logging.error('detectallnetworkforever函数报错了！')


    # 循环检测各设备网络连接状况
    def networkdiagnosisstart(self, mainUI, maindialog):
        try:
            self.dialog = maindialog
            self.main_UI = mainUI
            self.detectnetworkthread = threading.Thread(target=self.detectallnetworkforever)
            self.detectnetworkthread.daemon = True
            self.detectnetworkthread.start()
        except:
            logging.error("networkdiagnosisstart()运行异常，退出线程")
    #--------------------------------------------------------------------------------

    def detectinterfaceall(self):
        """监测每个模块通讯接口连接情况，"""
        interfacedict = {}
        list = []
        # list = [module.checkinterfacestatus() for module in self.modulelist if module.networkconnected ]
        for module in self.modulelist:
            if module.networkconnected:
                list.append(module.checkinterfacestatus())
        for statusdict in list:
            interfacedict.update(statusdict)
        #下面这一段代码是间接更新Instruments和LIS模块的接口状态
        for key in interfacedict:
            if key.startswith('Instruments'):
                name = key[11:]
                partnername = self.getpartnername(name, 'Instruments')
                if partnername:
                    if interfacedict[partnername] == 'ESTABLISHED':
                        interfacedict[key] = 'ESTABLISHED'
            elif key.startswith('LIS'):
                name = key[3:]
                partnername = self.getpartnername(name, 'LIS')
                if partnername:
                    if interfacedict[partnername] == 'ESTABLISHED':
                        interfacedict[key] = 'ESTABLISHED'
        ####################################################
        for interfacename,status in interfacedict.items():
            if self.allinterfacestatus.get(interfacename) != status:
                self.informUI(self.interfaceUI, interfacename, status)
        self.allinterfacestatus = interfacedict

    #通过接口名称查找与之对应的接口名称
    def getpartnername(self, name, modulename):
        ipandport = ''
        if modulename == 'Instruments':
            for module in self.modulelist:
                if module.name.upper() not in ['ATM','DMS','ADM','CENTRALINK','DATALINK','LIS']:
                    for interface in module.interfaceright:
                        if interface.find(name) > -1:
                            ipandport = interface.split(':', 1)[1].strip()
                            break
            for module in self.modulelist:
                if module.name.upper() in ['ATM','DMS', 'ADM', 'CENTRALINK', 'DATALINK']:
                    for interface in module.interfaceleft:
                        if ipandport == interface.split(':', 1)[1].strip():
                            return module.name + interface.split(':', 1)[0].strip()
        elif modulename == 'LIS':
            for module in self.modulelist:
                if module.name.upper() == "LIS":
                    for interface in module.interfaceleft:
                        if interface.find(name) > -1:
                            ipandport = interface.split(':', 1)[1].strip()
                            break
            for module in self.modulelist:
                if module.name.upper() in ['ATM','DMS', 'ADM', 'CENTRALINK', 'DATALINK']:
                    for interface in module.interfaceright:
                        if ipandport == interface.split(':', 1)[1].strip():
                            return module.name + interface.split(':', 1)[0].strip()
        return ''


    def detectinterfaceforever(self):
        """持续监控接口连接情况"""
        while True:
            try:
                self.detectinterfaceall()
                time.sleep(5)
            except:
                # print('detectinterfaceforever 函数报错了！')
                logging.error('detectinterfaceforever 函数报错了！')

    def interfacediagnosisstart(self, interfaceUI, dialogII):
        self.dialogII = dialogII
        self.interfaceUI = interfaceUI
        try:
            self.detectinterfacethread = threading.Thread(target=self.detectinterfaceforever)
            self.detectinterfacethread.daemon = True
            self.detectinterfacethread.start()
        except:
            # print('退出线程！')
            logging.error("interfacediagnosisstart()运行异常，退出线程")



if __name__ == "__main__":
    pass

