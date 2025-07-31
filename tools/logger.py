#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/7/29 12:29
# @Author : MaoYuan Xia
# @File   : logger.py
"""
import logging
import os
import sys
from datetime import datetime


def setup_logger(log_dir: str = "logs",
                 log_level: str = "INFO",
                 log_to_file: bool = True,
                 time_format: str = "%Y%m%d_%H%M%S"):
    """
    初始化全局日志记录器，使用时间格式作为文件名

    :param log_dir: 日志目录路径
    :param log_level: 日志级别(DEBUG/INFO/WARNING/ERROR)
    :param log_to_file: 是否保存到文件
    :param time_format: 文件名时间格式 (默认: 年月日_时分秒)
    """
    # 确保日志目录存在
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger("auto_test")
    logger.setLevel(log_level)

    # 避免重复添加处理器
    if not logger.handlers:
        # 创建标准格式
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-7s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 控制台处理器 - 始终启用
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 文件处理器 - 使用时间格式文件名
        if log_to_file:
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime(time_format)
            log_file = os.path.join(log_dir, f"test_{timestamp}.log")

            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger


# 全局日志记录器
logger = setup_logger(log_level="DEBUG")

# 直接导出常用方法
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
critical = logger.critical
exception = logger.exception


