import os
import time
import warnings
from base64 import b64decode as turin

from pywinauto import application as ctrl

warnings.simplefilter('ignore', category=UserWarning)
launch_script = """
cd "C:/Program Files (x86)"
taskkill /IM "saplogon.exe" /F
taskkill /IM "guixt.exe" /F
SAP\FrontEnd\SAPgui\sapshcut.exe -sysname={} -client=011 -user=tgt1hc -pw=secret
exit
"""


class Initializer:

    def __init__(self, logger, system):
        self.logger = logger
        self.system = system
        self.launch_p81_path = os.path.join(os.getcwd(), "launchSAP.cmd")
        self.clean_sys_tray = os.path.join(os.getcwd(), "clean_sys_tray.bat")

    def launch_sap(self):
        # Prepare cmd script to launch SAP GUI
        script = launch_script.format(self.system)

        # Replace the target string
        # Your SAP password in base64
        script = script.replace("secret", turin(
            "yourbase64pwd".encode("utf-8")).decode("utf-8"))

        with open(self.launch_p81_path, 'w') as oPath:
            oPath.writelines([script])

        self.logger.info("Starting the SAP GUI")
        os.system("start cmd /k launchSAP.cmd")

        # Control SAP Mutiple Logons GUI in case there is already a logon
        # somewhere
        try:
            time.sleep(15)  # Wait for SAP to popup
            sap_multiple = ctrl.Application().connect(
                title_re='.*License Information for Multiple Logons')
            self.logger.info("Start shutting down other logons")
            dlg = sap_multiple.window(
                title_re='.*License Information for Multiple Logons')
            dlg.type_keys("{TAB}{UP 2}{ENTER}")
        except Exception as e:
            self.logger.error(getattr(e, "message", repr(e)))
            self.logger.info("This SAP session is unique")

        # Clean secret file
        os.remove(self.launch_p81_path)

        # Refresh system tray
        os.system("start cmd /k clean_sys_tray.cmd")
