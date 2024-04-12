import os
import subprocess
from xmlrpc.server import SimpleXMLRPCServer

class satellite:

    def __init__(self):
        pass

    def get_netstat_info(self):
        # 执行netstat命令
        netstat_command = subprocess.Popen(['netstat', '-an'], \
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 读取netstat的输出
        output, _ = netstat_command.communicate()
        output_str = output.decode('utf-8', errors='ignore')
        return output_str

    def is_ip_reachable(self, ip_address):
        """
        检测指定IP地址是否可达
        :param ip_address: 要检测的IP地址
        :return: 如果IP地址可达，返回True；否则返回False
        """
        try:
            # 使用ping命令检测IP地址连通性
            ping_command = ["ping", "-n", "1", ip_address]
            ping_process = subprocess.Popen(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ping_output, ping_error = ping_process.communicate()

            output = ping_output.decode('utf-8', errors='ignore').strip()
            return output
        except:
            return ''
        
    def rebootRouter(self, process_name, routerPath):
        # 构造taskkill命令，使用/F参数强制结束进程，/IM参数指定进程名  
        cmd = ['taskkill', '/F', '/T', '/IM', process_name]  
        try:  
            # 执行命令并等待完成  
            subprocess.run(cmd, check=True)  
        except subprocess.CalledProcessError as e:  
            # 如果命令执行失败（例如进程不存在），则打印错误信息  
            pass
        
        # 检查文件是否存在  
        if not os.path.exists(routerPath):  
            # print(f"文件 {routerPath} 不存在。")  
            return False
        else:  
            # 使用subprocess调用bat文件  
            try:
                subprocess.Popen(["cmd", "/c", "start", routerPath], shell=True)
                return True
            except:
                return False
            
    def rebootOS(self):
        try:
            subprocess.Popen(["shutdown", "/r", "/t", '0'], shell=True)
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    server = SimpleXMLRPCServer(('', 18888))
    server.register_instance(satellite())
    server.serve_forever()