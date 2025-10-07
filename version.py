#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComicPacker 版本管理
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
__author__ = "ComicPacker Team"
__email__ = "comicpacker@example.com"
__description__ = "A tool for packing comic images into CBZ format"
__url__ = "https://github.com/yourusername/ComicPacker"

# 版本类型
VERSION_TYPE = "stable"  # stable, beta, alpha, dev

# 构建信息
BUILD_DATE = None  # 将在构建时自动设置
BUILD_COMMIT = None  # 将在构建时自动设置


def get_version():
    """获取版本号"""
    return __version__


def get_version_info():
    """获取版本信息元组"""
    return __version_info__


def get_full_version():
    """获取完整版本信息"""
    version_parts = [__version__]

    if VERSION_TYPE != "stable":
        version_parts.append(VERSION_TYPE)

    if BUILD_COMMIT:
        version_parts.append(f"commit-{BUILD_COMMIT[:8]}")

    return "-".join(version_parts)


def get_build_info():
    """获取构建信息"""
    info = {
        "version": __version__,
        "version_info": __version_info__,
        "version_type": VERSION_TYPE,
        "author": __author__,
        "email": __email__,
        "description": __description__,
        "url": __url__,
    }

    if BUILD_DATE:
        info["build_date"] = BUILD_DATE

    if BUILD_COMMIT:
        info["build_commit"] = BUILD_COMMIT

    return info


def print_version():
    """打印版本信息"""
    print(f"ComicPacker {get_full_version()}")
    print(f"作者: {__author__}")
    print(f"描述: {__description__}")
    print(f"项目地址: {__url__}")

    if BUILD_DATE:
        print(f"构建时间: {BUILD_DATE}")

    if BUILD_COMMIT:
        print(f"构建提交: {BUILD_COMMIT}")


if __name__ == "__main__":
    print_version()
