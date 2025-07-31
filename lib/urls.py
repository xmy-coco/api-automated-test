#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/7/29 18:22
# @Author : MaoYuan Xia
# @File   : urls.py
"""
class Service:
    BING_TEST_SERVICE = "bing.test.service"             # bing.test.service


# ------------------------- bing.test.service -------------------------
class BingTestService(Service):
    SEARCH = "https://{}/AS/Suggestions"
    GET = "https://{}/AS/Get"
    POST = "https://{}/AS/Post"
