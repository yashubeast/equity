import os
import logging
import colorlog
from datetime import datetime

from logging.handlers import RotatingFileHandler

os.makedirs("assets/logs", exist_ok=True)

_FMT = "%(asctime)s [%(log_color)s%(levelname)s%(reset)s] %(message)s"

stream = colorlog.StreamHandler()
stream.setFormatter(colorlog.ColoredFormatter(
    _FMT,
    log_colors={
        "DEBUG":    "orange",
        "INFO":     "green",
        "WARNING":  "yellow",
        "ERROR":    "red",
        "CRITICAL": "bold_red",
    }
))

timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
log_path = f"assets/logs/{timestamp}.log"
file = RotatingFileHandler(log_path, maxBytes=1_048_576, backupCount=3)
file.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
))

logging.basicConfig(level=logging.INFO, format=_FMT, handlers=[stream, file])

log = logging.getLogger("equity")
