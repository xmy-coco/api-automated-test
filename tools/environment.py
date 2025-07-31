#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time   : 2025/7/29 17:25
# @Author : MaoYuan Xia
# @File   : environment.py
"""
import os
from typing import Optional, Union


def get_env(
        name: Union[str, list[str]],
        default: Optional[str] = None,
        as_type: type = str
) -> Union[str, int, float, bool, None]:
    """
    获取环境变量（测试专用简化版）

    :param name: 环境变量名（或候选名列表）
    :param default: 不存在时的默认值
    :param as_type: 返回类型（str/int/float/bool）
    :return: 环境变量值或默认值

    布尔值转换规则：
    - True: "true", "1", "yes", "y", "on"（不区分大小写）
    - False: 其他任何值
    """
    # 支持多个候选环境变量名
    names = [name] if isinstance(name, str) else name

    # 尝试获取环境变量值
    value = None
    for var_name in names:
        value = os.getenv(var_name)
        if value is not None:
            break

    # 返回默认值如果未找到
    if value is None:
        return default

    # 类型转换
    try:
        if as_type == bool:
            return value.lower() in ("true", "1", "yes", "y", "on")
        if as_type == int:
            return int(value)
        if as_type == float:
            return float(value)
        return value
    except (ValueError, TypeError):
        return default


# 快捷方法
def get_env_bool(name: Union[str, list[str]], default: bool = False) -> bool:
    """获取布尔值环境变量"""
    return get_env(name, default, bool)


def get_env_int(name: Union[str, list[str]], default: int = 0) -> int:
    """获取整数环境变量"""
    return get_env(name, default, int)


def get_env_float(name: Union[str, list[str]], default: float = 0.0) -> float:
    """获取浮点数环境变量"""
    return get_env(name, default, float)


if __name__ == '__main__':
    print(get_env("TEST_ENV"))