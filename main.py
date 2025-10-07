# 导入必要的模块
from pack_comic import pack_comic_to_cbz, pack_compressed_comic_to_cbz
from version import get_full_version
import os
import argparse
import sys
import re
from pathlib import Path


def parse_extra_args(extra_args_str):
    """解析额外参数字符串"""
    if not extra_args_str:
        return {}

    extra_params = {}
    # 使用正则表达式匹配 key="value" 格式
    pattern = r'(\w+)="([^"]*)"'
    matches = re.findall(pattern, extra_args_str)

    for key, value in matches:
        # 尝试将数字字符串转换为整数
        try:
            if value.isdigit():
                extra_params[key] = int(value)
            else:
                extra_params[key] = value
        except ValueError:
            extra_params[key] = value

    return extra_params


def process_single_item(
    item_path, output_path, language, delete_original, verbose, extra_params
):
    """处理单个文件或文件夹"""
    if not os.path.exists(item_path):
        print(f"错误: 路径 '{item_path}' 不存在")
        return False

    try:
        # 处理ZIP文件
        if item_path.endswith(".zip"):
            if verbose:
                print(f"处理ZIP文件: {os.path.basename(item_path)}")

            # 获取文件名（不含扩展名）
            name = os.path.splitext(os.path.basename(item_path))[0]

            # 合并额外参数
            params = {
                "series": extra_params.get("series", name),
                "number": extra_params.get("number", 1),
                "language_iso": language,
                "title": extra_params.get("title", name),
                "remove_original_file": delete_original,
            }

            pack_compressed_comic_to_cbz(
                compressed_path=item_path,
                output_path=Path(output_path) / f"{name}.cbz",
                **params,
            )
            if verbose:
                print(f"✓ 成功处理: {os.path.basename(item_path)} -> {name}.cbz")
            return True

        # 处理文件夹
        elif os.path.isdir(item_path):
            if verbose:
                print(f"处理文件夹: {os.path.basename(item_path)}")

            name = os.path.basename(item_path)

            # 合并额外参数
            params = {
                "series": extra_params.get("series", name),
                "number": extra_params.get("number", 1),
                "language_iso": language,
                "title": extra_params.get("title", name),
                "remove_original_file": delete_original,
            }

            # 将文件夹中的漫画文件打包为CBZ格式
            pack_comic_to_cbz(
                comic_path=item_path,
                output_path=Path(output_path) / f"{name}.cbz",
                **params,
            )
            if verbose:
                print(f"✓ 成功处理: {name} -> {name}.cbz")
            return True

        else:
            if verbose:
                print(f"跳过不支持的文件: {os.path.basename(item_path)}")
            return False

    except Exception as e:
        print(f"错误处理 {os.path.basename(item_path)}: {e}")
        return False


def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description="ComicPacker - 将漫画文件打包成CBZ格式的工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 处理单个文件或文件夹
  python main.py -i ./漫画文件夹                    # 处理单个文件夹
  python main.py -i ./漫画.zip                      # 处理单个ZIP文件
  python main.py -i ./漫画文件夹 -o ./输出目录       # 指定输出目录
  
  # 批量处理模式
  python main.py -ip ./输入目录                     # 批量处理输入目录下的所有文件夹和ZIP文件
  python main.py -ip ./输入目录 -o ./输出目录        # 指定输出目录
  
  # 使用额外参数
  python main.py -i ./漫画文件夹 -e 'series="火影忍者", number="1", title="第一卷"'
  python main.py -ip ./输入目录 -e 'series="海贼王", language="ja-JP"'
  
  # 删除原始文件
  python main.py -i ./漫画文件夹 --delete-original
  python main.py -ip ./输入目录 --delo
  
  # 显示帮助信息
  python main.py --help
        """,
    )

    # 输入参数组
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "-i", "--input", help="需要打包的单个漫画文件夹或ZIP文件路径"
    )

    input_group.add_argument(
        "-ip",
        "--inputpath",
        default="./ComicPackerInput",
        help="需要打包的多个漫画文件夹所在的文件夹路径 (默认: ./ComicPackerInput)",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="./ComicPackerOutput",
        help="输出目录路径，用于存放打包后的CBZ文件 (默认: ./ComicPackerOutput)",
    )

    parser.add_argument(
        "--language", default="zh-CN", help="漫画语言代码 (默认: zh-CN)"
    )

    parser.add_argument(
        "--delete-original",
        "--delo",
        action="store_true",
        help="删除原始文件 (默认保留源文件)",
    )

    parser.add_argument("--verbose", action="store_true", help="显示详细处理信息")

    parser.add_argument(
        "-e",
        help='额外参数，格式: key1="value1", key2="value2" (例如: series="火影忍者", number="1")',
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"ComicPacker {get_full_version()}",
        help="显示版本信息并退出",
    )

    # 解析命令行参数
    args = parser.parse_args()

    # 解析额外参数
    extra_params = parse_extra_args(args.e)

    # 创建输出目录（如果不存在）
    os.makedirs(args.output, exist_ok=True)

    processed_count = 0
    error_count = 0

    if args.input:
        # 单个文件/文件夹模式
        if args.verbose:
            print(f"处理单个项目: {args.input}")
            print(f"输出目录: {args.output}")

        if process_single_item(
            args.input,
            args.output,
            args.language,
            args.delete_original,
            args.verbose,
            extra_params,
        ):
            processed_count += 1
        else:
            error_count += 1

    else:
        # 批量处理模式
        if not os.path.exists(args.inputpath):
            print(f"错误: 输入目录 '{args.inputpath}' 不存在")
            sys.exit(1)

        try:
            items = os.listdir(args.inputpath)
        except PermissionError:
            print(f"错误: 无法访问目录 '{args.inputpath}'，请检查权限")
            sys.exit(1)

        if args.verbose:
            print(f"开始批量处理目录: {args.inputpath}")
            print(f"输出目录: {args.output}")
            print(f"找到 {len(items)} 个项目")

        # 遍历输入目录中的所有项目
        for item in items:
            item_path = os.path.join(args.inputpath, item)

            if process_single_item(
                item_path,
                args.output,
                args.language,
                args.delete_original,
                args.verbose,
                extra_params,
            ):
                processed_count += 1
            else:
                error_count += 1

    # 显示处理结果
    print("\n处理完成!")
    print(f"成功处理: {processed_count} 个文件")
    if error_count > 0:
        print(f"处理失败: {error_count} 个文件")
    print(f"输出目录: {args.output}")


if __name__ == "__main__":
    main()
