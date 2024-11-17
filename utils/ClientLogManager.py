from loguru import logger
import os
import sys

from config.SystemConfig import config

class ClientLogManager:
    def __init__(self, log_file="ui_logs.log"):
        self.logger = logger
        self.log_dir = config.LOG_DIR
        self.log_file = log_file
        self.log_levels = ["trace", "debug", "info", "success", "warning", "error", "critical"]

        # 确保日志目录存在
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 移除所有默认的日志记录器，以避免重复记录
        logger.remove()

        # 配置文件日志记录，记录ERROR级别及以上的日志
        logger.add(
            os.path.join(self.log_dir, log_file),
            level="ERROR",
            rotation="00:00",
            retention="7 days",
            compression="zip",
        )

        # 配置控制台日志记录，显示DEBUG级别及以上的日志
        logger.add(
            sys.stdout,  # 使用sys.stdout打印到控制台
            level="DEBUG",
            colorize=True,
        )

    def log(self, level, msg, no=None):
        if level.lower() in self.log_levels:
            self.logger.log(level.upper(), msg)
        else:
            if no is not None:
                self.logger.level(level.upper(), no=no)
                self.logger.log(level.upper(), msg)
            self.logger.error("Unknown log level: {}".format(level))


client_logger = ClientLogManager()