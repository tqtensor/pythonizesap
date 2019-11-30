
import datetime
import os
import subprocess
import time
import warnings

from utils import load_config

warnings.simplefilter('ignore', category=UserWarning)
config_file = 'gui_controller.cfg'
config_path = os.path.join(os.getcwd(), config_file)
kill_process_script = """
cd "C:/Program Files (x86)"
taskkill /IM "{}" /F"""


class LX02():

    def __init__(self, logger):
        self.logger = logger
        self.process = 'excel.exe'
        self.sap = load_config(config_path)
        self.kill_process_path = os.path.join(os.getcwd(), "kill_process.cmd")
        self.script_template_path = os.path.join(
            os.getcwd(), r"guixt\LX02.txt")
        self.script_path = os.path.join(
            os.getcwd(), r"guixt\LX02Script.txt")

    def script_file(self):
        # Read in the file
        with open(self.script_template_path, "r") as file:
            file_content = file.read()

        # Prepare timestamp for filename
        timestamp = str(datetime.datetime.now())[2:19].replace(
            '-', '').replace(' ', '').replace(':', '')

        # Replace the target string
        file_content = file_content.replace("inWarehouse", '181')
        file_content = file_content.replace("inPlant", '1830')
        file_content = file_content.replace("inTimetamp", timestamp)

        # Write the file out again
        with open(self.script_path, "w") as file:
            file.write(file_content)

    def extract(self):
        cmd = "start guixt" + " input=" + \
            chr(34) + "OK: Process=" + self.script_path + chr(34)
        os.system(cmd)

    def kill_process(self):
         # Prepare cmd script to launch SAP GUI
        with open(self.kill_process_path, 'w') as oPath:
            oPath.writelines([kill_process_script.format(self.process)])

        self.logger.info("Killing process {}".format(self.process))
        try:
            p = subprocess.Popen(['kill_process.cmd'])
            _, _ = p.communicate()
        except Exception as e:
            self.logger.error(str(e))

        # Clean cmd file
        os.remove(self.kill_process_path)

    def etl(self):
        time.sleep(15)  # Wait for SAP GUI to be active
        self.kill_process()  # It is better to shutdown Excel while saving content
        self.logger.info("Extracting LX02")
        self.script_file()
        self.extract()
        time.sleep(40)  # Let SAP works bro
        self.logger.info("Complete extracting LX02")
        return True
