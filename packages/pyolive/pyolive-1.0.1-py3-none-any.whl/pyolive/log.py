import os
import sys
import socket
import logging
import logging.handlers
from .config import Config

# Logging 포맷 설정
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def create_logger(namespace=None, devel=False) -> logging.Logger:
    if not devel:
        config = Config('olive-env.conf')
        level = _get_log_level(config.get_value('log/worker/level'))
        count = _get_log_count(config.get_value('log/worker/rotate'))
        size = _get_log_bytes(config.get_value('log/worker/size'))
        path = _get_log_path(config.get_value('log/worker/path'))
        name = _get_log_name(namespace, path)

        logger = logging.getLogger('ovd-worker')
        logger.setLevel(level)
        file_handler = logging.handlers.RotatingFileHandler(filename=name, maxBytes=size, backupCount=count)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    else:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        stdout_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stdout_handler)
    return logger


def _get_log_level(level_str):
    if level_str == 'info':
        level = logging.INFO
    elif level_str == 'warn':
        level = logging.WARNING
    elif level_str == 'error':
        level = logging.ERROR
    else:
        level = logging.DEBUG
    return level


def _get_log_count(rotate_str):
    return int(rotate_str)


def _get_log_bytes(size_str):
    i = size_str.find('kb')
    if i > 0:
        return int(size_str[:i]) * 1024
    i = size_str.find('mb')
    if i > 0:
        return int(size_str[:i]) * 1024 * 1024
    i = size_str.find('gb')
    if i > 0:
        return int(size_str[:i]) * 1024 * 1024 * 1024
    return 0


def _get_log_path(dir_str):
    return os.path.join(os.getenv('OLIVE_HOME'), 'logs', dir_str)


def _get_log_name(namespace, path):
    file = namespace + '@' + socket.gethostname() + '.log'
    return os.path.join(path, file)


