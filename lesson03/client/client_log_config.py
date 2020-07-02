"""Настройки модуля логирования."""

import logging
from datetime import datetime
import sys

logger = logging.getLogger('client')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

fh = logging.FileHandler(f"{datetime.now().date()}client.log",
                         encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

console_client_handler = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
console_client_handler = logging.StreamHandler()
console_client_handler.setLevel(logging.DEBUG)
logger.addHandler(console_client_handler)
logger.setLevel(logging.DEBUG)

