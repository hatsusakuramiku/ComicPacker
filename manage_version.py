#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本管理脚本
用于管理ComicPacker的版本号
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime


def get_current_version():
    """获取当前版本号"""
    try:
        from version import __version__

        return __version__
    except ImportError:
        return "0.0.0"


def get_git_commit():
    """获取当前Git提交哈希"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def update_version_file(major=None, minor=None, patch=None, version_type="stable"):
    """更新版本文件"""
    version_file = Path("version.py")

    if not version_file.exists():
        print("❌ 未找到version.py文件!")
        return False

    # 读取当前版本
    current_version = get_current_version()
    version_parts = [int(x) for x in current_version.split(".")]

    # 更新版本号
    if major is not None:
        version_parts[0] = major
        version_parts[1] = 0  # 重置次要版本
        version_parts[2] = 0  # 重置补丁版本
    elif minor is not None:
        version_parts[1] = minor
        version_parts[2] = 0  # 重置补丁版本
    elif patch is not None:
        version_parts[2] = patch

    new_version = ".".join(map(str, version_parts))
    new_version_info = tuple(version_parts)

    # 读取文件内容
    content = version_file.read_text(encoding="utf-8")

    # 更新版本号
    content = re.sub(
        r'__version__ = "[^"]*"', f'__version__ = "{new_version}"', content
    )

    # 更新版本信息元组
    content = re.sub(
        r"__version_info__ = \([^)]*\)",
        f"__version_info__ = {new_version_info}",
        content,
    )

    # 更新版本类型
    content = re.sub(
        r'VERSION_TYPE = "[^"]*"', f'VERSION_TYPE = "{version_type}"', content
    )

    # 更新构建日期
    build_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = re.sub(r"BUILD_DATE = None", f'BUILD_DATE = "{build_date}"', content)

    # 更新构建提交
    commit = get_git_commit()
    if commit:
        content = re.sub(r"BUILD_COMMIT = None", f'BUILD_COMMIT = "{commit}"', content)

    # 写入文件
    version_file.write_text(content, encoding="utf-8")

    print(f"✅ 版本已更新为: {new_version}")
    print(f"版本类型: {version_type}")
    if commit:
        print(f"Git提交: {commit[:8]}")

    return True


def show_version():
    """显示当前版本信息"""
    try:
        from version import print_version

        print_version()
    except ImportError:
        print("❌ 无法导入版本信息!")


def show_help():
    """显示帮助信息"""
    print("ComicPacker 版本管理工具")
    print("=" * 40)
    print()
    print("使用方法:")
    print("  python manage_version.py show                    # 显示当前版本")
    print(
        "  python manage_version.py patch                  # 增加补丁版本 (1.0.0 -> 1.0.1)"
    )
    print(
        "  python manage_version.py minor                  # 增加次要版本 (1.0.0 -> 1.1.0)"
    )
    print(
        "  python manage_version.py major                  # 增加主要版本 (1.0.0 -> 2.0.0)"
    )
    print("  python manage_version.py set 1.2.3              # 设置特定版本")
    print("  python manage_version.py beta                   # 设置为beta版本")
    print("  python manage_version.py alpha                  # 设置为alpha版本")
    print("  python manage_version.py stable                 # 设置为stable版本")
    print()
    print("示例:")
    print("  python manage_version.py patch                  # 1.0.0 -> 1.0.1")
    print("  python manage_version.py minor                  # 1.0.1 -> 1.1.0")
    print("  python manage_version.py set 2.0.0-beta.1       # 设置为2.0.0-beta.1")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "show":
        show_version()
    elif command == "patch":
        current = get_current_version()
        parts = [int(x) for x in current.split(".")]
        update_version_file(patch=parts[2] + 1)
    elif command == "minor":
        current = get_current_version()
        parts = [int(x) for x in current.split(".")]
        update_version_file(minor=parts[1] + 1)
    elif command == "major":
        current = get_current_version()
        parts = [int(x) for x in current.split(".")]
        update_version_file(major=parts[0] + 1)
    elif command == "set":
        if len(sys.argv) < 3:
            print("❌ 请指定版本号!")
            return

        version = sys.argv[2]
        if not re.match(r"^\d+\.\d+\.\d+", version):
            print("❌ 版本号格式不正确! 应为 x.y.z")
            return

        parts = [int(x) for x in version.split(".")[:3]]
        update_version_file(major=parts[0], minor=parts[1], patch=parts[2])
    elif command in ["beta", "alpha", "stable"]:
        update_version_file(version_type=command)
    elif command in ["help", "-h", "--help"]:
        show_help()
    else:
        print(f"❌ 未知命令: {command}")
        show_help()


if __name__ == "__main__":
    main()
