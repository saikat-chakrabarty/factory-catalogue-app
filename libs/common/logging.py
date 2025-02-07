import logging
import sys

def configure_logging(log_level: str, environment: str):
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(log_level.upper())
