# ComicPacker 使用说明

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
ComicPacker版本: 1.0.0
构建时间: 2025-10-07 20:09:54
Python版本: 3.10.11
PyInstaller版本: 6.14.1
