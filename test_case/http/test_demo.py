#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/7/29 12:34
# @Author : MaoYuan Xia
# @File   : test_demo.py
"""
import pytest
import allure
from tools.file_reader import FileReader as f
from tools.logger import setup_logger


logger = setup_logger(log_level="INFO")


@allure.feature("测试 feature")
class TestDemo:
    @allure.title("用例名称")
    @pytest.mark.parametrize("test_data", f.read_file("test_data/bing_test.json"))
    def test_demo(self, bing_test_client, test_data):
        r = bing_test_client.get_bing(
            data = test_data["data"],
            headers = test_data["headers"],
        )
        logger.info(r)
        assert True

    def setup_class(self):
        pass


    def teardown_class(self):
        pass