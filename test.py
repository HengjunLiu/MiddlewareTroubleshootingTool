# import xmlrpc.client

# server_url = 'http://192.168.3.115:18888'
# try:
#     # 连接到XML-RPC服务器
#     # server_url = "http://localhost:18888"
#     proxy = xmlrpc.client.ServerProxy(server_url)
#     # 调用方法并获取结果
#     result = proxy.is_ip_reachable('192.168.1.1')
# except Exception as e:
#     print(e)
# else:
#     print(result)

import os

list1=[1,2,3,4,5]
list2=[6,7,8,9,10]

print(list1 + list2)