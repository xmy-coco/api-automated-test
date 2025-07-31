#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/7/29 13:22
# @Author : MaoYuan Xia
# @File   : file_reader.py
"""
import os
import json
import yaml
from pathlib import Path
from typing import Union, Any
from tools.logger import setup_logger


logger = setup_logger(log_level="DEBUG")


# 获取项目根目录（此文件所在位置）
PROJECT_ROOT = Path(os.path.abspath(os.path.dirname(__file__))).parent


# 常用目录预设（可选）
class PathPreset:
    TEST_DATA = PROJECT_ROOT / "test_data"
    CONFIG = PROJECT_ROOT / "config"
    MODELS = PROJECT_ROOT / "models"
    LOGS = PROJECT_ROOT / "logs"

    @staticmethod
    def from_string(path_str: str) -> Path:
        """将字符串路径转换为Path对象"""
        return Path(path_str)


class FileReader:
    @staticmethod
    def _resolve_path(path: Union[str, Path]) -> Path:
        """解析路径：支持相对路径、绝对路径和预设路径"""
        # 如果是字符串路径
        if isinstance(path, str):
            # 检查是否是预设路径别名（如 "DATA"）
            if hasattr(PathPreset, path.upper()):
                return getattr(PathPreset, path.upper())

            # 否则转换为Path对象
            path = Path(path)

        # 如果是绝对路径，直接返回
        if path.is_absolute():
            return path

        # 否则，视为相对于项目根目录的路径
        return PROJECT_ROOT / path

    @staticmethod
    def read_file(file_path: Union[str, Path]) -> Any:
        """
        读取JSON/YAML文件

        参数:
            file_path: 文件路径（绝对路径、相对路径或预设路径别名）

        返回:
            文件内容（字典、列表等）
        """
        path = FileReader._resolve_path(file_path)

        # 确保是文件
        if not path.is_file():
            raise FileNotFoundError(f"路径不是文件或不存在: {path}")

        suffix = path.suffix.lower()

        with open(path, 'r', encoding='utf-8') as f:
            if suffix == '.json':
                return json.load(f)
            elif suffix in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            else:
                raise ValueError(f"不支持的文件类型: {suffix} (仅支持 .json, .yaml, .yml)")

    @staticmethod
    def read_json(file_path: Union[str, Path]) -> Any:
        """读取JSON文件的快捷方法"""
        return FileReader.read_file(file_path)

    @staticmethod
    def read_yaml(file_path: Union[str, Path]) -> Any:
        """读取YAML文件的快捷方法"""
        return FileReader.read_file(file_path)


if __name__ == '__main__':
    print(PathPreset.TEST_DATA)
    f = FileReader.read_file(r"config/shanghai.json")
    print(f)