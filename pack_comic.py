from pathlib import Path
from typing import Optional
import tempfile
import zipfile

from cbz.comic import ComicInfo
from cbz.constants import PageType, YesNo, Manga, AgeRating, Format
from cbz.page import PageInfo

IMAGE_EXTENSIONS_SET = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".tif"}


def get_image_files(folder_path: Path) -> list[Path]:
    """从文件夹中获取所有图片文件。

    Args:
        folder_path (Path): 文件夹路径

    Returns:
        list[Path]: 图片文件路径列表
    """
    # 支持的图片格式
    # image_extensions = {
    #     ".jpg",
    #     ".jpeg",
    #     ".png",
    #     ".gif",
    #     ".bmp",
    #     ".webp",
    #     ".tiff",
    #     ".tif",
    # }

    # 获取文件夹中的所有文件并过滤出图片文件
    all_files = list(folder_path.iterdir())
    image_files = sorted(
        [path for path in all_files if path.suffix.lower() in IMAGE_EXTENSIONS_SET],
        key=lambda p: p.name
    )

    return image_files


def pack_comic(
    comic_path: Path,
    output_path: Optional[Path] = None,
    show: bool = False,
    title: Optional[str] = None,
    remove_original_file: bool = False,
    **kwargs,
) -> None:
    """将漫画文件夹打包成CBZ格式的漫画文件。

    Args:
        comic_path (Path): 包含漫画图片的文件夹路径
        output_path (Path, optional): 输出CBZ文件的路径。如果未指定，将在脚本所在目录创建同名CBZ文件
        show (bool, optional): 是否显示漫画信息。默认为False
        title (str, optional): 漫画标题。如果未指定，将使用文件夹名称
        remove_original_file (bool, optional): 打包完成后是否删除源文件。默认为False

    Returns:
        None: 函数将直接创建CBZ文件
    """
    # 如果未指定标题，使用文件夹名称作为标题
    title = title or Path(comic_path).name
    # 设置输出路径，如果未指定则使用默认路径
    output_path = (
        Path(output_path).with_suffix(".cbz")
        if output_path
        else Path(__file__).parent / f"{title}.cbz"
    )

    # 获取图片文件并转换为PageInfo对象
    image_paths = get_image_files(comic_path)
    pages = [PageInfo.load(path=path, type=PageType.STORY) for path in image_paths]

    # 创建ComicInfo对象
    comic = ComicInfo.from_pages(
        pages=pages,
        title=title,
        **kwargs,
    )

    # 如果需要显示漫画信息
    if show:
        comic.show()

    # 将漫画打包并写入CBZ文件
    output_path.write_bytes(comic.pack())

    # 如果需要删除源文件
    if remove_original_file:
        import shutil
        shutil.rmtree(comic_path)


def pack_comic_to_cbz(
    comic_path: Path,
    output_path: Optional[Path] = None,
    show: bool = False,
    title: Optional[str] = None,
    series: Optional[str] = None,
    number: Optional[int] = None,
    language_iso: str = "zh-CN",
    format: Format = Format.WEB_COMIC,
    black_white: YesNo = YesNo.NO,
    manga: Manga = Manga.YES,
    age_rating: AgeRating = AgeRating.PENDING,
    remove_original_file: bool = False,
) -> None:
    """将漫画文件夹打包成CBZ格式的漫画文件。

    Args:
        comic_path (Path): 包含漫画图片的文件夹路径
        output_path (Path, optional): 输出CBZ文件的路径。如果未指定，将在脚本所在目录创建同名CBZ文件
        show (bool, optional): 是否显示漫画信息。默认为False
        title (str, optional): 漫画标题。如果未指定，将使用文件夹名称
        series (str, optional): 漫画系列名称
        number (int, optional): 漫画卷号
        language_iso (str, optional): 语言代码。默认为"zh-CN"
        format (Format, optional): 漫画格式。默认为WEB_COMIC
        black_white (YesNo, optional): 是否为黑白漫画。默认为NO
        manga: (Manga, optional): 是否为日式漫画。默认为YES
        age_rating (AgeRating, optional): 年龄分级。默认为PENDING
        remove_original_file (bool, optional): 打包完成后是否删除源文件。默认为False

    Returns:
        None: 函数将直接创建CBZ文件
    """
    # 如果未指定标题，使用文件夹名称作为标题
    title = title or Path(comic_path).name
    # 设置输出路径，如果未指定则使用默认路径
    output_path = (
        Path(output_path).with_suffix(".cbz")
        if output_path
        else Path(__file__).parent / f"{title}.cbz"
    )

    # 获取图片文件并转换为PageInfo对象
    image_paths = get_image_files(comic_path)
    pages = [PageInfo.load(path=path, type=PageType.STORY) for path in image_paths]

    # 创建ComicInfo对象
    comic = ComicInfo.from_pages(
        pages=pages,
        title=title,
        series=series,
        number=number,
        language_iso=language_iso,
        format=format,
        black_white=black_white,
        manga=manga,
        age_rating=age_rating,
    )

    # 如果需要显示漫画信息
    if show:
        comic.show()

    # 将漫画打包并写入CBZ文件
    output_path.write_bytes(comic.pack())

    # 如果需要删除源文件
    if remove_original_file:
        import shutil

        shutil.rmtree(comic_path)


def pack_compressed_comic_to_cbz(
    compressed_path: Path,
    output_path: Optional[Path] = None,
    show: bool = False,
    title: Optional[str] = None,
    series: Optional[str] = None,
    number: Optional[int] = None,
    language_iso: str = "zh-CN",
    format: Format = Format.WEB_COMIC,
    black_white: YesNo = YesNo.NO,
    manga: Manga = Manga.YES,
    age_rating: AgeRating = AgeRating.PENDING,
    remove_original_file: bool = False,
) -> None:
    """将压缩包格式的漫画转换为CBZ格式的漫画文件。

    Args:
        compressed_path (Path): 压缩包格式的漫画文件路径
        output_path (Path, optional): 输出CBZ文件的路径。如果未指定，将在脚本所在目录创建同名CBZ文件
        show (bool, optional): 是否显示漫画信息。默认为False
        title (str, optional): 漫画标题。如果未指定，将使用压缩包名称
        series (str, optional): 漫画系列名称
        number (int, optional): 漫画卷号
        language_iso (str, optional): 语言代码。默认为"zh-CN"
        format (Format, optional): 漫画格式。默认为WEB_COMIC
        black_white (YesNo, optional): 是否为黑白漫画。默认为NO
        manga: (Manga, optional): 是否为日式漫画。默认为YES
        age_rating (AgeRating, optional): 年龄分级。默认为PENDING
        remove_original_file (bool, optional): 打包完成后是否删除源文件。默认为False

    Returns:
        None: 函数将直接创建CBZ文件
    """
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # 解压文件到临时目录
        with zipfile.ZipFile(compressed_path, "r") as zip_ref:
            zip_ref.extractall(temp_path)

        # 如果未指定标题，使用压缩包名称（不含扩展名）作为标题
        title = title or compressed_path.stem

        # 调用现有的打包函数处理解压后的文件
        pack_comic_to_cbz(
            comic_path=temp_path,
            output_path=output_path,
            show=show,
            title=title,
            series=series,
            number=number,
            language_iso=language_iso,
            format=format,
            black_white=black_white,
            manga=manga,
            age_rating=age_rating,
            remove_original_file=remove_original_file,
        )

        # 如果需要删除源文件
        if remove_original_file:
            try:
                compressed_path.unlink()
            except Exception as e:
                try:
                    import os

                    os.remove(compressed_path)
                except Exception as e:
                    import shutil

                    shutil.rmtree(compressed_path)
