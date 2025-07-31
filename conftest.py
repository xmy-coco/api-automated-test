#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/7/29 13:18
# @Author : MaoYuan Xia
# @File   : conftest.py
"""
import pytest
import allure
from tools.environment import get_env
from tools.file_reader import FileReader as f
from lib.urls import BingTestService
from client.bing_test_client import BingTestClient
from tools.logger import setup_logger


logger = setup_logger(log_level="DEBUG")


@pytest.fixture(scope="session")
def TEST_ENV():
    # 获取测试环境初始化对应测试数据
    logger.debug(get_env("TEST_ENV"))
    return get_env("TEST_ENV")

@pytest.fixture(scope="session")
def TEST_CLUSTER():
    logger.debug(get_env("TEST_CLUSTER"))
    return get_env("TEST_CLUSTER")

@pytest.fixture(scope="session")
def TEST_IDC():
    logger.debug(get_env("TEST_IDC"))
    idc = get_env("TEST_IDC")
    if "shanghai" in idc:
        return "shanghai"
    elif "beijing" in idc:
        return "beijing"
    elif "japan" in idc:
        return "japan"
    return get_env("TEST_IDC")


@pytest.fixture(scope="session")
def bing_test_client(TEST_IDC, TEST_ENV):
    config = f.read_file("config/{}.json".format(TEST_IDC))
    config = config[TEST_ENV][BingTestService.BING_TEST_SERVICE]
    return BingTestClient(
        host = config["host"],
        env = config["env"],
        idc = config["idc"],
        cluster = config["cluster"],
    )


if __name__ == '__main__':
    cfg = f.read_file(r"config/shanghai.json")
    logger.info(cfg)