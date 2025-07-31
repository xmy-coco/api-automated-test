#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/7/29 16:24
# @Author : MaoYuan Xia
# @File   : bing_test_client.py
"""
from typing import Dict
from client.base_client import HttpClient
from lib.urls import BingTestService
from tools.logger import setup_logger


logger = setup_logger(log_level="DEBUG")


class BingTestClient(HttpClient):
    def __init__(self,
                 psm: str = BingTestService.BING_TEST_SERVICE,
                 idc: str = None,
                 host: str = None ,
                 env: str = None,
                 cluster: str = None,
                 **kwargs):
        super().__init__()  # 初始化
        self.psm = psm
        self.idc = idc
        self.host = host
        self.env = env
        self.cluster = cluster

    def get_bing(self, data: Dict, headers: Dict) -> Dict:
        url = BingTestService.SEARCH.format(self.host)
        r = self.get(endpoint=url, params=data, headers=headers)
        return r.json()








if __name__ == '__main__':
    ...