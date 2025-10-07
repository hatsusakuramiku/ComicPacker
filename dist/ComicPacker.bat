@echo off
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
