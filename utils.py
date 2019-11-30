import configparser
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def load_config(config_path):
    config = configparser.ConfigParser()
    cfgfile = open(Path(config_path))
    config.read_file(cfgfile)
    deploy_mode = config.get("environment", "deployment_mode")
    sap = config.get(deploy_mode, "sap")
    return sap


def get_logger(log_path, max_bytes=1000000, backup_count=5):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: %(levelname)s: %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        handlers=[
            logging.StreamHandler(),
            RotatingFileHandler(
                Path(log_path),
                maxBytes=max_bytes,
                backupCount=backup_count)])
    return logging.getLogger()
