"""Настройки модуля логирования."""
import logging
from datetime import datetime

server_logger = logging.getLogger('server')
server_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")
fhs = logging.FileHandler(f"{datetime.now().date()}server.log", encoding='utf-8')
fhs.setLevel(logging.DEBUG)
fhs.setFormatter(server_formatter)
server_logger.addHandler(fhs)
server_logger.setLevel(logging.DEBUG)

console_server_hanler = logging.StreamHandler()
console_server_hanler.setLevel(logging.DEBUG)
console_server_hanler.setFormatter(server_formatter)
server_logger.addHandler(console_server_hanler)
server_logger.setLevel(logging.DEBUG)