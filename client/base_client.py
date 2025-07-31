#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/7/29 16:15
# @Author : MaoYuan Xia
# @File   : base_client.py
"""
import requests
import json
import os
import time
from typing import Optional, Dict, Any, Tuple, Union
from requests.exceptions import RequestException
from tools.logger import setup_logger


logger = setup_logger(log_level="DEBUG")


class HttpClient:
    """
    HTTP客户端封装，简化API请求操作

    功能特点：
    - 统一请求入口（支持GET/POST/PUT/DELETE/PATCH）
    - 自动JSON解析
    - 请求重试机制
    - 超时控制
    - 自动记录请求日志
    - 异常统一处理
    - 支持文件上传
    - 响应结果验证
    """

    def __init__(self,
                 base_url: str = "",
                 default_headers: Optional[Dict] = None,
                 timeout: int = 10,
                 max_retries: int = 3,
                 retry_interval: int = 2,
                 raise_for_status: bool = True):
        """
        初始化HTTP客户端

        :param base_url: 基础URL（可选）
        :param default_headers: 默认请求头
        :param timeout: 请求超时时间（秒）
        :param max_retries: 最大重试次数
        :param retry_interval: 重试间隔时间（秒）
        :param raise_for_status: 是否在非2xx响应时抛出异常
        """
        self.base_url = base_url.rstrip("/")
        self.default_headers = default_headers or {"Content-Type": "application/json"}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.raise_for_status = raise_for_status
        self.session = requests.Session()

    def request(self,
                method: str,
                endpoint: str,
                params: Optional[Dict] = None,
                json_data: Optional[Union[Dict, list]] = None,
                data: Optional[Dict] = None,
                files: Optional[Dict] = None,
                headers: Optional[Dict] = None,
                **kwargs) -> requests.Response:
        """
        发送HTTP请求（核心方法）

        :param method: HTTP方法（GET/POST/PUT/DELETE等）
        :param endpoint: 请求端点（相对路径）
        :param params: 查询参数
        :param json_data: JSON请求体
        :param data: form-data请求体
        :param files: 上传文件
        :param headers: 请求头
        :return: 响应对象
        """
        # 构建完整URL
        url = f"{self.base_url}/{endpoint.lstrip('/')}" if self.base_url else endpoint

        # 合并请求头
        final_headers = {**self.default_headers, **(headers or {})}

        # 记录请求信息
        logger.debug(f"HTTP Request: {method} {url}")
        if params: logger.debug(f"Params: {params}")
        if json_data: logger.debug(f"JSON Body: {json.dumps(json_data, indent=2)}")
        if data: logger.debug(f"Form Data: {data}")

        # 重试逻辑
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    data=data,
                    files=files,
                    headers=final_headers,
                    timeout=self.timeout,
                    **kwargs
                )

                # 记录响应信息
                self._log_response(response, attempt)

                # 检查状态码
                if self.raise_for_status:
                    response.raise_for_status()

                return response

            except RequestException as e:
                # 最后一次尝试仍然失败
                if attempt == self.max_retries:
                    logger.error(f"Request failed after {self.max_retries} retries: {str(e)}")
                    raise

                logger.warning(f"Request failed (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                time.sleep(self.retry_interval)

    def _log_response(self, response: requests.Response, attempt: int):
        """记录响应日志"""
        try:
            # 尝试解析JSON响应
            response_data = response.json()
            data_str = json.dumps(response_data, indent=2, ensure_ascii=False)
            content_type = "JSON"
        except json.JSONDecodeError:
            # 非JSON响应
            data_str = response.text[:1000]  # 截断长文本
            content_type = "TEXT"

        logger.info(f"HTTP Response [{response.status_code}] (Attempt: {attempt + 1})")
        logger.debug(f"Response Content-Type: {content_type}")
        logger.debug(f"Response Body: {data_str}")

    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送GET请求"""
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json_data: Optional[Dict] = None, data: Optional[Dict] = None,
             **kwargs) -> requests.Response:
        """发送POST请求"""
        return self.request("POST", endpoint, json_data=json_data, data=data, **kwargs)

    def put(self, endpoint: str, json_data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送PUT请求"""
        return self.request("PUT", endpoint, json_data=json_data, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """发送DELETE请求"""
        return self.request("DELETE", endpoint, **kwargs)

    def patch(self, endpoint: str, json_data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """发送PATCH请求"""
        return self.request("PATCH", endpoint, json_data=json_data, **kwargs)

    def upload_file(self, endpoint: str, file_path: str, field_name: str = "file", **kwargs) -> requests.Response:
        """上传文件"""
        with open(file_path, 'rb') as f:
            files = {field_name: (os.path.basename(file_path), f)}
            return self.request("POST", endpoint, files=files, **kwargs)

    def get_json(self, *args, **kwargs) -> Union[Dict, list]:
        """发送请求并返回解析后的JSON"""
        response = self.request(*args, **kwargs)
        return response.json()

    def get_text(self, *args, **kwargs) -> str:
        """发送请求并返回响应文本"""
        response = self.request(*args, **kwargs)
        return response.text

    def add_header(self, key: str, value: str):
        """添加默认请求头"""
        self.default_headers[key] = value

    def remove_header(self, key: str):
        """移除默认请求头"""
        if key in self.default_headers:
            del self.default_headers[key]

    def set_auth(self, auth_type: str, token: str):
        """设置认证信息"""
        if auth_type.lower() == "bearer":
            self.add_header("Authorization", f"Bearer {token}")
        elif auth_type.lower() == "basic":
            self.add_header("Authorization", f"Basic {token}")
        else:
            self.add_header("Authorization", token)


# 使用示例
if __name__ == "__main__":
    # 创建客户端实例
    client = HttpClient(
        base_url="https://api.example.com",
        default_headers={"User-Agent": "TestClient/1.0"},
        timeout=15,
        max_retries=2
    )

    # 设置认证
    client.set_auth("Bearer", "your_token_here")

    try:
        # GET请求示例
        response = client.get("/users", params={"page": 1, "limit": 10})
        users = response.json()
        print(f"获取到 {len(users)} 个用户")

        # POST请求示例
        new_user = {"name": "John", "email": "john@example.com"}
        result = client.post("/users", json_data=new_user).json()
        print(f"创建用户ID: {result['id']}")

        # 文件上传示例
        upload_res = client.upload_file("/upload", "test.txt")
        print(f"文件上传结果: {upload_res.status_code}")

    except Exception as e:
        print(f"请求失败: {str(e)}")