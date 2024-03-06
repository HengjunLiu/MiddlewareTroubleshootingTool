import os
import win32serviceutil
import win32service
import sys
import tkinter as tk
from tkinter import messagebox

class ServiceInstaller(object):
    def __init__(self, service_name, display_name, exe_path):
        self.service_name = service_name
        self.display_name = display_name
        self.exe_path = exe_path

    def install(self):
        try:
            win32serviceutil.InstallService(
                pythonClassString=None,
                serviceName=self.service_name,
                displayName=self.display_name,
                exeName=self.exe_path
            )
            # Open the service
            hscm = win32service.OpenSCManager(None,None,win32service.SC_MANAGER_ALL_ACCESS)
            hs = win32service.OpenService(hscm, self.service_name, win32service.SERVICE_ALL_ACCESS)
            # Change the service start type to auto start
            win32service.ChangeServiceConfig(hs, win32service.SERVICE_NO_CHANGE, win32service.SERVICE_AUTO_START,
                                             win32service.SERVICE_NO_CHANGE, None, None, 0, None, None, None, None)
            win32service.CloseServiceHandle(hs)
            win32service.CloseServiceHandle(hscm)
            messagebox.showinfo("Success", f"Service {self.service_name} installed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install service: {e}")

    def uninstall(self):
        try:
            win32serviceutil.RemoveService(self.service_name)
            messagebox.showinfo("Success", f"Service {self.service_name} removed successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove service: {e}")

def main():
    # Set default values for service_name, display_name, and exe_path if no arguments are provided.
    if len(sys.argv) == 1:
        current_path = os.getcwd()
        exe_name = 'Satellite.exe'
        service_name = 'SatelliteServer'
        display_name = 'SatelliteServer'
        exe_path = os.path.join(current_path,exe_name)
    else:
        service_name = sys.argv[1]
        display_name = sys.argv[2]
        exe_path = sys.argv[3]

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    installer = ServiceInstaller(service_name, display_name, exe_path)
    installer.install()  # Install the service with the provided details.
    # root.mainloop()  # Start the TUI event loop to display messages.
    root.destroy()  # Close the Tkinter window


if __name__ == '__main__':
    main()
