# ComicPacker

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/ComicPacker)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

ComicPacker 是一个用于将漫画文件打包成 CBZ 格式的 Python 工具。它支持将文件夹中的漫画图片或压缩包格式的漫画转换为标准的 CBZ 格式，并自动添加漫画元数据信息。

## 功能特点

- 支持将文件夹中的漫画图片打包为 CBZ 格式
- 支持将 ZIP 格式的压缩包转换为 CBZ 格式
- 自动添加漫画元数据（标题、系列名称、卷号等）
- 支持设置漫画语言、格式、黑白/彩色等属性
- 批量处理功能，可同时处理多个漫画文件
- 支持命令行参数，灵活配置
- 可打包成独立的可执行文件
- 支持单个文件处理和批量处理两种模式

## 安装说明

1. 确保已安装 Python 3.6 或更高版本
2. 安装依赖包：

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：Python 脚本运行

#### 单个文件/文件夹处理模式

```bash
# 处理单个文件夹
python main.py -i ./漫画文件夹

# 处理单个ZIP文件
python main.py -i ./漫画.zip

# 指定输出目录
python main.py -i ./漫画文件夹 -o ./输出目录

# 使用额外参数
python main.py -i ./漫画文件夹 -e 'series="火影忍者", number="1", title="第一卷"'
```

#### 批量处理模式

```bash
# 批量处理输入目录下的所有文件夹和ZIP文件
python main.py -ip ./输入目录

# 指定输出目录
python main.py -ip ./输入目录 -o ./输出目录

# 使用额外参数
python main.py -ip ./输入目录 -e 'series="海贼王", language="ja-JP"'
```

### 方法二：可执行文件运行

```bash
# 处理单个文件/文件夹
./dist/ComicPacker.exe -i ./漫画文件夹

# 批量处理
./dist/ComicPacker.exe -ip ./输入目录

# 显示帮助信息
./dist/ComicPacker.exe --help
```

### 命令行参数说明

#### 输入参数（必须选择其中一个）

- `-i, --input`: 需要打包的单个漫画文件夹或 ZIP 文件路径
- `-ip, --inputpath`: 需要打包的多个漫画文件夹所在的文件夹路径 (默认: ./ComicPackerInput)

#### 输出参数

- `-o, --output`: 输出目录路径，用于存放打包后的 CBZ 文件 (默认: ./ComicPackerOutput)

#### 其他参数

- `--language`: 漫画语言代码 (默认: zh-CN)
- `--delete-original` / `--delo`: 删除原始文件 (默认保留源文件)
- `--verbose`: 显示详细处理信息
- `-e`: 额外参数，格式: key1="value1", key2="value2" (例如: series="火影忍者", number="1")

#### 额外参数支持

- `series`: 漫画系列名称
- `number`: 漫画卷号
- `title`: 漫画标题
- `language`: 漫画语言代码

## 打包成可执行文件

### 自动打包

运行打包脚本：

```bash
python build_exe.py
```

这将自动安装 PyInstaller 并生成可执行文件。

### 手动打包

1. 安装 PyInstaller：

   ```bash
   pip install pyinstaller
   ```

2. 执行打包命令：

   ```bash
   pyinstaller --onefile --console --name=ComicPacker main.py
   ```

3. 可执行文件将生成在 `dist` 目录中

## 目录结构

- `main.py`: 主程序入口
- `pack_comic.py`: 核心打包功能模块
- `build_exe.py`: 打包脚本
- `requirements.txt`: 项目依赖
- `dist/`: 打包后的可执行文件目录

## 支持的元数据

- 标题（Title）
- 系列名称（Series）
- 卷号（Number）
- 语言（Language）
- 格式（Format）
- 黑白/彩色（Black & White）
- 漫画类型（Manga）
- 年龄分级（Age Rating）

## 注意事项

- 确保输入路径存在且有读取权限
- 输出目录会自动创建（如果不存在）
- 支持的图片格式包括：JPG、PNG、GIF 等常见图片格式
- 默认语言设置为中文（zh-CN）
- 默认漫画类型设置为日式漫画（Manga）
- 默认保留源文件，使用 `--delete-original` 或 `--delo` 参数可删除源文件
- 单个处理模式和批量处理模式是互斥的，必须选择其中一个

## 错误处理

程序会显示详细的错误信息，包括：

- 输入路径不存在
- 文件权限问题
- 处理失败的文件列表
- 成功处理的文件数量

## 示例输出

```bash
开始批量处理目录: ./ComicPackerInput
输出目录: ./ComicPackerOutput
找到 3 个项目
处理文件夹: 火影忍者第一卷
✓ 成功处理: 火影忍者第一卷 -> 火影忍者第一卷.cbz
处理ZIP文件: 海贼王第二卷.zip
✓ 成功处理: 海贼王第二卷.zip -> 海贼王第二卷.cbz
跳过不支持的文件: readme.txt

处理完成!
成功处理: 2 个文件
输出目录: ./ComicPackerOutput
```

## 版本管理

ComicPacker 使用语义化版本控制 (Semantic Versioning)。

### 查看版本信息

```bash
# 显示当前版本
python manage_version.py show

# 在程序中使用
python main.py --version
```

### 版本管理命令

```bash
# 增加补丁版本 (1.0.0 -> 1.0.1)
python manage_version.py patch

# 增加次要版本 (1.0.0 -> 1.1.0)
python manage_version.py minor

# 增加主要版本 (1.0.0 -> 2.0.0)
python manage_version.py major

# 设置特定版本
python manage_version.py set 1.2.3
```

### 项目结构

```markdown
ComicPacker/
├── main.py              # 主程序入口
├── pack_comic.py        # 核心打包功能
├── version.py           # 版本管理
├── manage_version.py    # 版本管理脚本
├── build_exe.py         # 构建脚本
├── requirements.txt     # 依赖列表
├── README.md           # 项目说明
```
