import os
import time

import schedule

from utils import get_logger, load_config

# Declare all paths
config_file = 'main.cfg'
config_path = os.path.join(os.getcwd(), config_file)
sap = load_config(config_path)

# Init logging instance
log_path = os.path.join(os.getcwd(), r"log\main.log")
logger = get_logger(log_path)


def job_1hour():
    from init import Initializer
    Initializer(logger, 'P81: Produktion GS').launch_sap()

    logger.info("Starting LX02 job")
    # Re-import class to run the latest deployed sourcecode
    from lx02 import LX02
    LX02(logger).etl()


def scheduled_etl():
    print("""
        PythonizedSAP connector developed by victurtle
        **********************************************
              **********************************
                   ************************
                        **************
                             ****
        """)

    # Schedule jobs
    schedule.every(1).hour.do(job_1hour)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    scheduled_etl()
