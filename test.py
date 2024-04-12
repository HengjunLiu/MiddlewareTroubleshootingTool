import os
import subprocess

process_name = 'cmd.exe'
routerPath = r'D:\Users\Desktop\test.lnk'

def rebootRouter(process_name, routerPath):
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
            print(f"文件 {routerPath} 不存在。")  
            return False
        else:  
            # 使用subprocess调用bat文件  
            try:
                subprocess.Popen(["cmd", "/c", "start", routerPath], shell=True)
                print('已执行')
                return True
            except:
                print('执行失败')
                return False
            
            
rebootRouter(process_name, routerPath)