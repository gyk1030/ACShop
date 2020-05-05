
import logging
import os
from ACShop.settings import LINUX_ENV
from ACShop.settings import LOG_PATH


class _Logging(object):
    debug = logging.DEBUG
    info = logging.INFO
    warning = logging.WARNING
    error = logging.ERROR
    critical = logging.CRITICAL

    def __init__(self, level):
        if not os.path.exists(LOG_PATH):  # 无文件时创建
            if LINUX_ENV:
                path = '/'.join(LOG_PATH.split('/')[:-1])
            else:
                path = '\\'.join(LOG_PATH.split('\\')[:-1])
            if not os.path.isdir(path): # 路径不存在时创建
                os.mkdir(path)

            f = open(LOG_PATH,'w',encoding='utf-8')
            f.close()

        self._fileHandler = logging.FileHandler(LOG_PATH, 'a',
                                                encoding='utf-8')  # 指定保存文件路径
        self._fileHandler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s'))  # 设置格式
        self.logger = logging.Logger('v1', level=getattr(self, level, 'error') if hasattr(self,
                                                                                          level) else self.error)  # 用反射获取日志级别，默认error
        self.logger.addHandler(self._fileHandler)


class Logger():
    def error(self, msg):
        return _Logging('error').logger.error(msg)

    def info(self, msg):
        return _Logging('info').logger.info(msg)

    def warning(self, msg):
        return _Logging('warning').logger.warning(msg)

    def critical(self, msg):
        return _Logging('critical').logger.critical(msg)

    def debug(self, msg):
        return _Logging('debug').logger.debug(msg)
