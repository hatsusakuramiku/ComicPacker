#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ComicPacker 打包脚本
用于将项目打包成可执行文件
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 导入版本信息
try:
    from version import get_version, get_full_version, get_build_info
except ImportError:
    # 如果无法导入版本信息，使用默认值
    def get_version():
        return "1.0.0"

    def get_full_version():
        return "1.0.0"

    def get_build_info():
        return {"version": "1.0.0", "version_info": (1, 0, 0)}


def check_dependencies() -> bool:
    """检查并安装项目依赖"""
    print("检查项目依赖...")

    # 检查requirements.txt是否存在
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("❌ 未找到requirements.txt文件!")
        return False

    try:
        # 安装项目依赖
        print("正在安装项目依赖...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        print("✅ 项目依赖安装成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 项目依赖安装失败: {e}")
        return False


def install_pyinstaller() -> bool:
    """安装PyInstaller"""
    print("正在安装PyInstaller...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pyinstaller>=5.0.0"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        print("✅ PyInstaller安装成功!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller安装失败: {e}")
        return False


def validate_build_environment() -> bool:
    """验证构建环境"""
    print("验证构建环境...")

    # 检查主程序文件
    if not Path("main.py").exists():
        print("❌ 未找到main.py文件!")
        return False

    # 检查pack_comic.py文件
    if not Path("pack_comic.py").exists():
        print("❌ 未找到pack_comic.py文件!")
        return False

    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要Python 3.8或更高版本!")
        return False

    print("✅ 构建环境验证通过!")
    return True


def build_exe() -> bool:
    """构建可执行文件"""
    print("开始构建可执行文件...")

    # 优化的PyInstaller命令参数
    cmd = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--console",  # 控制台应用
        "--name=ComicPacker",  # 可执行文件名称
        "--distpath=./dist",  # 输出目录
        "--workpath=./build",  # 工作目录
        "--specpath=./",  # spec文件目录
        "--clean",  # 清理临时文件
        "--noconfirm",  # 不确认覆盖
        "--optimize=2",  # Python优化级别
        "--strip",  # 去除调试信息
        "--noupx",  # 禁用UPX压缩（避免兼容性问题）
        "--add-data=requirements.txt;.",  # 包含requirements.txt
        "main.py",  # 主程序文件
    ]

    try:
        print("执行PyInstaller命令...")
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

        if result.returncode == 0:
            print("✅ 构建成功!")
            return True
        else:
            print("❌ 构建失败!")
            print(f"错误输出: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ 构建过程中发生异常: {e}")
        return False


def create_batch_file():
    """创建批处理文件用于Windows用户"""
    batch_content = """@echo off
chcp 65001 >nul
title ComicPacker - 漫画打包工具

echo.
echo ========================================
echo    ComicPacker - 漫画打包工具
echo ========================================
echo.
echo 使用示例:
echo   ComicPacker.exe                    # 使用默认设置
echo   ComicPacker.exe -i ./input         # 指定输入目录
echo   ComicPacker.exe -o ./output        # 指定输出目录
echo   ComicPacker.exe --delete-original  # 删除原始文件
echo   ComicPacker.exe --help             # 显示帮助信息
echo.
echo 支持的输入格式:
echo   - 图片文件夹 (jpg, png, gif, bmp, webp, tiff)
echo   - 压缩包文件 (zip, rar, 7z)
echo.
echo 输出格式: CBZ (Comic Book ZIP)
echo.
echo ========================================
echo.

:menu
echo 请选择操作:
echo 1. 运行 ComicPacker
echo 2. 显示帮助信息
echo 3. 退出
echo.
set /p choice=请输入选择 (1-3): 

if "%choice%"=="1" (
    echo.
    echo 启动 ComicPacker...
    ComicPacker.exe
    goto end
) else if "%choice%"=="2" (
    echo.
    ComicPacker.exe --help
    echo.
    pause
    goto menu
) else if "%choice%"=="3" (
    goto end
) else (
    echo 无效选择，请重新输入。
    echo.
    goto menu
)

:end
echo.
echo 感谢使用 ComicPacker!
pause
"""

    try:
        with open("dist/ComicPacker.bat", "w", encoding="utf-8") as f:
            f.write(batch_content)
        print("✅ 已创建批处理文件: dist/ComicPacker.bat")
    except Exception as e:
        print(f"❌ 创建批处理文件失败: {e}")


def create_readme():
    """创建使用说明文件"""
    readme_content = """# ComicPacker 使用说明

## 简介
ComicPacker 是一个用于将漫画图片打包成CBZ格式的工具。

## 功能特性
- 支持多种图片格式 (JPG, PNG, GIF, BMP, WEBP, TIFF)
- 支持压缩包格式输入 (ZIP, RAR, 7Z)
- 自动过滤非图片文件
- 生成标准CBZ格式输出
- 支持自定义漫画元数据

## 使用方法

### 命令行使用
```bash
# 基本用法
ComicPacker.exe

# 指定输入目录
ComicPacker.exe -i ./input_folder

# 指定输出目录
ComicPacker.exe -o ./output_folder

# 删除原始文件
ComicPacker.exe --delete-original

# 显示帮助信息
ComicPacker.exe --help
```

### 批处理文件使用
双击 `ComicPacker.bat` 文件，按照菜单提示操作。

## 支持的输入格式
- **图片文件夹**: 包含图片文件的文件夹
- **压缩包**: ZIP, RAR, 7Z 等压缩格式

## 输出格式
- **CBZ**: Comic Book ZIP 格式，兼容大多数漫画阅读器

## 注意事项
1. 确保输入文件夹中包含有效的图片文件
2. 非图片文件会被自动过滤
3. 输出文件会覆盖同名的现有文件
4. 默认保留源文件，使用 --delete-original 参数可删除源文件

## 版本信息
ComicPacker版本: {comicpacker_version}
构建时间: {build_time}
Python版本: {python_version}
PyInstaller版本: {pyinstaller_version}
"""

    try:
        # 获取构建信息
        import datetime

        build_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        # 尝试获取PyInstaller版本
        try:
            import PyInstaller

            pyinstaller_version = PyInstaller.__version__
        except ImportError:
            pyinstaller_version = "未知"

        readme_content = readme_content.format(
            comicpacker_version=get_full_version(),
            build_time=build_time,
            python_version=python_version,
            pyinstaller_version=pyinstaller_version,
        )

        with open("dist/README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("✅ 已创建使用说明: dist/README.txt")
    except Exception as e:
        print(f"❌ 创建使用说明失败: {e}")


def cleanup_build_files():
    """清理构建文件"""
    print("清理之前的构建文件...")

    cleanup_paths = ["dist", "build", "ComicPacker.spec"]
    for path in cleanup_paths:
        if os.path.exists(path):
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                print(f"✅ 已清理: {path}")
            except Exception as e:
                print(f"⚠️  清理 {path} 时出现警告: {e}")


def main():
    """主函数"""
    print("=" * 60)
    print("           ComicPacker 打包工具")
    print(f"           版本: {get_full_version()}")
    print("=" * 60)
    print()

    # 步骤1: 验证构建环境
    if not validate_build_environment():
        print("\n❌ 构建环境验证失败，请检查上述错误!")
        return False

    # 步骤2: 检查并安装依赖
    if not check_dependencies():
        print("\n❌ 依赖安装失败，请检查网络连接和requirements.txt文件!")
        return False

    # 步骤3: 检查PyInstaller
    try:
        import PyInstaller  # noqa: F401

        print("✅ PyInstaller已安装")
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        if not install_pyinstaller():
            print("\n❌ PyInstaller安装失败!")
            return False

    # 步骤4: 清理构建文件
    cleanup_build_files()

    # 步骤5: 构建可执行文件
    print("\n" + "=" * 60)
    print("开始构建可执行文件...")
    print("=" * 60)

    if not build_exe():
        print("\n❌ 构建失败!")
        return False

    # 步骤6: 创建辅助文件
    print("\n创建辅助文件...")
    create_batch_file()
    create_readme()

    # 步骤7: 显示结果
    print("\n" + "=" * 60)
    print("🎉 打包完成!")
    print("=" * 60)
    print(f"📁 可执行文件位置: {os.path.abspath('dist/ComicPacker.exe')}")
    print(f"📄 批处理文件位置: {os.path.abspath('dist/ComicPacker.bat')}")
    print(f"📖 使用说明位置: {os.path.abspath('dist/README.txt')}")
    print()
    print("🚀 使用方法:")
    print("  命令行: ./dist/ComicPacker.exe --help")
    print("  图形界面: 双击 dist/ComicPacker.bat")
    print()
    print("=" * 60)

    return True


if __name__ == "__main__":
    main()
