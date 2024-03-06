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


if __name__ == '__main__':
    server = SimpleXMLRPCServer(('', 18888))
    server.register_instance(satellite())
    server.serve_forever()