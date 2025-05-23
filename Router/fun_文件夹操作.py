"""素材文件夹操作"""

import contextlib
import shutil
import subprocess
from pathlib import Path

import pythoncom
from colorama import Fore, Style
from PIL import Image
from pydantic import BaseModel
from tqdm import tqdm
from win10toast import ToastNotifier
from win32com.client import Dispatch

from MaterialEdit import AIFile, PSFile
from MaterialEdit.fun_ppt_删除备注 import fun_处理所有PPT
from MaterialEdit.fun_ppt导出图片 import PPT导出图片
from MaterialEdit.fun_PS文件处理.fun_对比所有导出的图片 import fun_所有广告图片
from MaterialEdit.fun_PS文件处理3.fun_删除文字图层广告 import DeleteImageName
from MaterialEdit.fun_图片编辑.fun_图片扩大粘贴 import fun_图片扩大粘贴
from MaterialEdit.fun_图片编辑.fun_蜘蛛水印.fun_蜘蛛水印 import fun_蜘蛛水印
from MaterialEdit.fun_文件夹操作 import ImageCopyToPreview
from MaterialEdit.fun_文件夹操作.fun_AI批量导出图片重命名 import (
    AIBatchExportImageRename,
)
from MaterialEdit.fun_文件夹操作.fun_AI文件重命名 import fun_ai文件重命名
from MaterialEdit.fun_文件夹操作.fun_CMYK图片转RGB import fun_CMYK转RGB
from MaterialEdit.fun_文件夹操作.fun_SD生成图片改名 import SDPicReName
from MaterialEdit.fun_文件夹操作.fun_享设计文件夹重构 import fun_享设计文件夹重构
from MaterialEdit.fun_文件夹操作.fun_删除AI对应的PNG图片 import fun_删除AI对应的PNG文件
from MaterialEdit.fun_文件夹操作.fun_删除EPS文件 import fun_删除EPS文件
from MaterialEdit.fun_文件夹操作.fun_删除享设计文件夹结构的预览图 import (
    fun_删除享设计文件夹结构的预览图,
)
from MaterialEdit.fun_文件夹操作.fun_删除图片边框 import fun_删除图片边框
from MaterialEdit.fun_文件夹操作.fun_删除广告文件 import fun_删除广告文件
from MaterialEdit.fun_文件夹操作.fun_删除文件夹 import fun_删除文件夹
from MaterialEdit.fun_文件夹操作.fun_删除素材文件夹所有图片 import (
    fun_删除素材文件夹所有图片,
)
from MaterialEdit.fun_文件夹操作.fun_删除预览小图 import fun_删除预览小图
from MaterialEdit.fun_文件夹操作.fun_制作享设计大图 import fun_享设计制作预览图
from MaterialEdit.fun_文件夹操作.fun_制作版权图片 import fun_制作版权图片
from MaterialEdit.fun_文件夹操作.fun_图片添加白色背景 import fun_图片添加白色背景
from MaterialEdit.fun_文件夹操作.fun_子目录psd重命名 import fun_子目录PSD重命名
from MaterialEdit.fun_文件夹操作.fun_子目录图片重命名 import fun_子目录图片重命名
from MaterialEdit.fun_文件夹操作.fun_子目录拼接图片 import fun_子目录拼接图片
from MaterialEdit.fun_文件夹操作.fun_打开所有子文件夹 import open_sub_path
from MaterialEdit.fun_文件夹操作.fun_打开没有预览图的AI文件 import OpenNoPngAIFile
from MaterialEdit.fun_文件夹操作.fun_打开没有预览图的PSD文件 import OpenNoImagePsdFiles
from MaterialEdit.fun_文件夹操作.fun_按数字分类 import fun_按数字分类
from MaterialEdit.fun_文件夹操作.fun_文件夹内文件夹重命名 import (
    fun_文件夹内文件夹重命名,
)
from MaterialEdit.fun_文件夹操作.fun_文件夹初始化 import fun_文件夹初始化
from MaterialEdit.fun_文件夹操作.fun_文件重命名 import fun_文件重命名
from MaterialEdit.fun_文件夹操作.fun_生成SKP导出命令 import fun_生成SKP批量导出脚本
from MaterialEdit.fun_文件夹操作.fun_目录内放置广告 import fun_目录内放置广告
from MaterialEdit.fun_文件夹操作.fun_移动AI文件和对应的图片到子目录 import (
    MoveAIToSubPath,
)
from MaterialEdit.fun_文件夹操作.fun_移动PSD到子目录 import fun_移动PSD到子目录
from MaterialEdit.fun_文件夹操作.fun_移动到效果图 import fun_移动到效果图
from MaterialEdit.fun_文件夹操作.fun_移动到根目录 import fun_移动到根目录
from MaterialEdit.fun_文件夹操作.fun_素材图水印2 import fun_素材图水印2
from MaterialEdit.fun_文件夹操作.fun_透明图转白底 import fun_透明图转白底
from MaterialEdit.fun_文件夹操作.fun_遍历指定文件 import rglob
from MaterialEdit.fun_遍历图片 import fun_遍历图片
from MaterialEdit.setting import HOME_UPDATE_FOLDER, OUT_PATH
from mylog import mylogger

toaster = ToastNotifier()


def fun_通知(msg: str) -> None:
    """发送windows通知"""
    toaster.show_toast(title="素材编辑程序", msg=msg, threaded=True, duration=2)


class RequestMaterialPathActionModel(BaseModel):
    """素材文件夹操作模型."""

    action: str
    shop_name: str
    root_path: str

    file_start_stem: str
    path_start_stem: str


def fun_material_path_action(item: RequestMaterialPathActionModel) -> dict[str, str]:
    """操作素材文件夹函数."""
    mylogger.info(item)

    material_structure = fun_文件夹初始化(root_path=item.root_path)

    match item.action:
        case "打开所有子文件夹":
            open_sub_path(material_path=material_structure.material_path)

        case "打开素材文件夹":
            subprocess.Popen(
                args=f"explorer {material_structure.material_path.replace('/', '\\')}",
                shell=True,
            )

        case "打开预览图文件夹":
            subprocess.run(
                args=f"explorer {material_structure.preview_path.replace('/', '\\')}",
                check=False,
                shell=True,
            )

        case "打开效果图文件夹":
            if Path(material_structure.effect_path) is True:
                subprocess.run(
                    args=f"explorer {material_structure.effect_path.replace('/', '\\')}",
                    check=False,
                    shell=True,
                )

        case "打开桌面上传文件夹":
            subprocess.run(
                args=f"explorer {HOME_UPDATE_FOLDER.as_posix().replace('/', '\\')}",
                check=False,
                shell=True,
            )

        case "删除效果图":
            fun_删除文件夹(folder=material_structure.effect_path)

        case "删除预览图":
            fun_删除文件夹(folder=material_structure.preview_path)

        case "解压ZIP":
            in_file_list = [
                zippath.absolute().as_posix()
                for zippath in rglob(
                    folder=material_structure.material_path,
                    suffix=[".zip", ".rar", ".7z"],
                )
            ]
            args = [
                "C:\\Program Files\\Bandizip\\Bandizip.exe",
                "bx",
                "-y",
                "-target:name",
            ]
            args.extend(in_file_list)
            res = subprocess.run(
                args=args,
                check=False,
            )
            msg = "解压文件成功" if res.returncode == 0 else "解压文件失败"
            mylogger.info("Process completed successfully.")

            for infile in in_file_list:
                msg = (
                    f"删除文件{infile}"
                    if Path(infile).exists() is True
                    else f"文件不存在{infile}"
                )
                mylogger.info(msg)
                Path(infile).unlink()

        case "移动到根目录":
            fun_移动到根目录(folder=material_structure.material_path)
            if Path(material_structure.preview_path).exists() is True:
                fun_移动到根目录(folder=material_structure.preview_path)

        case "删除广告文件":
            fun_删除广告文件(folder=material_structure.material_path)

        case "文件重命名":
            fun_文件重命名(
                folder=material_structure.material_path,
                preview_path=material_structure.preview_path,
                shop_name=item.shop_name,
                num=int(item.file_start_stem),
            )

        case "删除素材文件夹内所有图片":
            fun_删除素材文件夹所有图片(folder=material_structure.material_path)

        case "复制图片到预览图":
            ac = ImageCopyToPreview(
                folder_path=material_structure.material_path,
                preview_path=material_structure.preview_path,
            )
            ac.main()

        case "移动到效果图":
            fun_移动到效果图(
                material_path=material_structure.material_path,
                effect_path=material_structure.effect_path,
            )

        case "素材图水印":
            fun_素材图水印2(
                material_path=material_structure.material_path,
                shop_name=item.shop_name,
            )

        case "按数字分类":
            fun_按数字分类(material_path=material_structure.material_path)
            fun_按数字分类(material_path=material_structure.preview_path)

        case "AI-导出图片":
            all_file = []
            all_file.extend(rglob(material_structure.material_path, [".ai", ".eps"]))

            pythoncom.CoInitialize()
            app = Dispatch("Illustrator.Application")
            for in_file in tqdm(all_file, ncols=100, desc="处理AI文件"):
                pic_state = False
                for suffix in [".jpg", ".jpeg", ".png"]:
                    png_path = in_file.with_suffix(suffix)
                    if png_path.exists() is True:
                        pic_state = True

                if pic_state is False:
                    all_png = [
                        in_png.stem
                        for in_png in rglob(
                            material_structure.material_path,
                            [".png", ".jpeg", ".jpg"],
                        )
                    ]

                    for in_png in all_png:
                        if in_file.stem in in_png:
                            pic_state = True

                if pic_state is False:
                    AIFile(
                        in_file.as_posix(),
                        app,
                        shop_name=item.shop_name,
                    ).fun_导出PNG()

            pythoncom.CoUninitialize()

            for in_file in Path(material_structure.material_path).rglob("*"):
                if in_file.is_dir() and in_file.name in ["3000w", "2000w"]:
                    shutil.rmtree(in_file.as_posix())

        case "PSD-删除广告-导出图片-添加广告":
            # 获取所有PSD
            all_file = []
            all_file.extend(rglob(material_structure.material_path, [".psd", ".psb"]))

            # 清空OUT_PATH
            for in_file in OUT_PATH.iterdir():
                if in_file.is_file():
                    in_file.unlink()
                else:
                    shutil.rmtree(in_file.as_posix())

            pythoncom.CoInitialize()
            ad_pic_list = fun_所有广告图片()
            for in_file in tqdm(all_file, ncols=100, desc="删除广告导出图片\t"):
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    # 如果是4KB的PSD不处理
                    min_size = 4096
                    if in_file.stat().st_size == min_size:
                        continue

                    # 大小判断 超大的不处理
                    size = in_file.stat().st_size / 1024 / 1024
                    max_size = 300
                    if size > max_size:
                        continue

                    PSFile(
                        ps_path=in_file.as_posix(),
                        tb_name=item.shop_name,
                        ad_pic_list=ad_pic_list,
                    ).run_删除广告导出PNG()

            pythoncom.CoUninitialize()

        case "PSD-图层名删除广告-导出图片-添加广告":
            pythoncom.CoInitialize()
            DeleteImageName(
                material_path=Path(material_structure.material_path),
                shop_name=item.shop_name,
            ).main()
            pythoncom.CoUninitialize()

        case "PSD-导出图片-添加广告":
            # 获取所有PSD
            all_file = []
            all_file.extend(rglob(material_structure.material_path, [".psd", ".psb"]))

            pythoncom.CoInitialize()

            for in_file in tqdm(all_file, ncols=100, desc="导出图片 添加广告\t"):
                in_file: Path
                pic_exists = False
                for pic_suffix in [".jpg", ".png"]:
                    png_path = in_file.with_suffix(pic_suffix)
                    if png_path.exists() is True:
                        pic_exists = True

                if pic_exists is False:
                    min_size = 4096
                    if in_file.stat().st_size == min_size:
                        in_file.unlink()
                    try:
                        PSFile(
                            ps_path=in_file.as_posix(),
                            tb_name=item.shop_name,
                            ad_pic_list=[],
                        ).run_导出图片添加广告()
                    except Exception as e:
                        msg = f"错误的PSD文件:{in_file},{e}"
                        mylogger.info(msg)

            pythoncom.CoUninitialize()

        case "PSD-删除错误PSD-导出图片-添加广告":
            # 获取所有PSD
            all_file = []
            all_file.extend(rglob(material_structure.material_path, [".psd", ".psb"]))

            pythoncom.CoInitialize()

            for in_file in tqdm(all_file, ncols=100, desc="导出图片 添加广告\t"):
                in_file: Path
                pic_exists = False
                for pic_suffix in [".jpg", ".png"]:
                    png_path = in_file.with_suffix(pic_suffix)
                    if png_path.exists() is True:
                        pic_exists = True

                if pic_exists is False:
                    min_size = 4096
                    if in_file.stat().st_size == min_size:
                        in_file.unlink()
                    try:
                        PSFile(
                            ps_path=in_file.as_posix(),
                            tb_name=item.shop_name,
                            ad_pic_list=[],
                        ).run_导出图片添加广告()
                    except Exception as e:
                        msg = f"错误的PSD文件:{in_file},{e}"
                        mylogger.info(msg)
                        in_file.unlink()

            pythoncom.CoUninitialize()

        case "PSD-图层改名-导出图片-添加广告":
            all_file = []
            all_file.extend(rglob(material_structure.material_path, [".psd", ".psb"]))

            pythoncom.CoInitialize()
            for in_file in tqdm(all_file, ncols=100, desc="导出图片，添加广告\t"):
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    min_size = 4096
                    if in_file.stat().st_size == min_size:
                        in_file.unlink()
                    PSFile(
                        ps_path=in_file.as_posix(),
                        tb_name=item.shop_name,
                        ad_pic_list=[],
                    ).run_图层改名_导出图片()

            pythoncom.CoUninitialize()

        case "PSD-导出图片":
            all_file = []
            all_file.extend(rglob(material_structure.material_path, [".psd", ".psb"]))

            pythoncom.CoInitialize()

            for in_file in tqdm(all_file, desc="导出图片", ncols=100):
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    min_size = 4096
                    if in_file.stat().st_size == min_size:
                        msg = f"{Fore.RED}错误的PSD文件{Style.RESET_ALL} {in_file}"
                        mylogger.info(msg=msg)
                        continue

                    with contextlib.suppress(Exception):
                        PSFile(
                            ps_path=in_file.as_posix(),
                            tb_name=item.shop_name,
                            ad_pic_list=[],
                        ).run_导出图片()

            pythoncom.CoUninitialize()

        case "删除EPS文件":
            fun_删除EPS文件(material_path=material_structure.material_path)

        case "PPT-导出图片":
            all_file = []
            all_file.extend(rglob(material_structure.material_path, [".ppt", ".pptx"]))

            for in_file in tqdm(all_file, ncols=100, desc="PPT导出图片"):
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is False:
                    PPT导出图片(ppt_path=in_file).main()

        case "PPT-删除备注":
            fun_处理所有PPT(material_path=material_structure.material_path)

        case "子目录内文件移动到根":
            for in_path in Path(material_structure.material_path).iterdir():
                fun_移动到根目录(in_path.as_posix())

        case "子目录重命名":
            fun_文件夹内文件夹重命名(
                material_path=material_structure.material_path,
                shop_name=item.shop_name,
                num=int(item.path_start_stem),
            )

        case "图片添加白色背景":
            fun_图片添加白色背景(material_path_text=material_structure.material_path)

        case "删除ZIP文件":
            for in_file in tqdm(
                rglob(material_structure.material_path, [".zip", ".rar"]),
                ncols=100,
                desc="删除ZIP文件",
            ):
                in_file.unlink()

        case "AI文件重命名":
            fun_ai文件重命名(material_path=material_structure.material_path)

        case "删除AI对应的PNG文件":
            fun_删除AI对应的PNG文件(material_path=material_structure.material_path)

        case "享设计制作预览图":
            fun_享设计制作预览图(
                material_path=material_structure.material_path,
                shop_name=item.shop_name,
            )

        case "打开没有预览图的PPT":
            all_file = rglob(
                folder=material_structure.material_path,
                suffix=[".ppt", ".pptx"],
            )
            for in_file in all_file:
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is not True:
                    subprocess.run(
                        args=["start", in_file.as_posix()],
                        shell=True,
                        check=False,
                    )

        case "打开没有预览图的SKP":
            all_file = rglob(folder=material_structure.material_path, suffix=[".skp"])
            for in_file in all_file:
                png_path = in_file.with_suffix(".png")
                if png_path.exists() is not True:
                    subprocess.run(args=in_file.as_posix(), check=False)

        case "eps转ai":
            pythoncom.CoInitialize()
            app = Dispatch("Illustrator.Application")
            for in_file in Path(material_structure.material_path).rglob("*"):
                if in_file.suffix.lower() in [".eps"] and in_file.is_file():
                    ai_path = in_file.with_suffix(".ai")

                    doc = app.Open(in_file.as_posix())
                    doc.SaveAs(ai_path)
                    doc.Close(2)
                    in_file.unlink()

        case "享设计文件夹重构":
            fun_享设计文件夹重构(material_path=material_structure.material_path)

        case "删除图片边框":
            fun_删除图片边框(material_path=material_structure.material_path)

        case "子目录PSD重命名":
            fun_子目录PSD重命名(material_path=material_structure.material_path)

        case "子目录图片重命名":
            fun_子目录图片重命名(material_path=material_structure.material_path)

        case "子目录拼接图片":
            fun_子目录拼接图片(material_path=material_structure.material_path)

        case "目录内放置广告":
            fun_目录内放置广告(
                material_path=material_structure.material_path,
                shop_name=item.shop_name,
            )

        case "效果图蜘蛛水印":
            for in_file in fun_遍历图片(
                folder=material_structure.effect_path,
                used_image_number=0,
                image_sort=True,
            ):
                im = Image.open(in_file)
                if im.mode != "rgba":
                    im = im.convert("RGBA")

                im = fun_蜘蛛水印(im)
                Path(in_file).unlink()
                im.save(Path(in_file).with_suffix(".png"))

        case "效果图扩大":
            for in_file in fun_遍历图片(
                folder=material_structure.effect_path,
                used_image_number=0,
                image_sort=True,
            ):
                im = Image.open(in_file)
                if im.mode.lower() != "rgba":
                    im = im.convert("RGBA")

                im = fun_图片扩大粘贴(
                    im,
                    width=int(im.width * 1.1),
                    height=int(im.height * 1.1),
                    left="center",
                    top="center",
                    background_color=(255, 255, 255, 0),
                )

                im.save(in_file)

        case "效果图webp转png":
            for in_file in rglob(
                folder=material_structure.effect_path,
                suffix=[".webp"],
            ):
                im = Image.open(in_file.as_posix())
                if im.mode != "RGBA":
                    im = im.convert("RGBA")

                im.save(in_file.with_suffix(".png"))
                in_file.unlink()

        case "AI批量导出图片重命名":
            for in_file in rglob(
                folder=material_structure.material_path,
                suffix=[".ai"],
            ):
                obj = AIBatchExportImageRename(ai_file=in_file)
                obj.fun_jpg_重命名()

        case "生成SKP导出命令":
            fun_生成SKP批量导出脚本(in_path=material_structure.material_path)

        case "AI导出效果图改名":
            sd_rename = SDPicReName(
                effect_path=material_structure.effect_path,
                material_path=material_structure.material_path,
                shop_name=item.shop_name,
            )
            sd_rename.main()

        case "打开没有预览图的AI文件":
            pythoncom.CoInitialize()
            OpenNoPngAIFile(in_path=material_structure.material_path).main()

        case "打开没有预览图的PSD文件":
            pythoncom.CoInitialize()
            OpenNoImagePsdFiles(material_path=material_structure.material_path).main()

        case "CMYK转RGB":
            pythoncom.CoInitialize()
            fun_CMYK转RGB(
                material_path=material_structure.material_path,
                preview_path=material_structure.preview_path,
            )

        case "AI文件移动到子目录":
            MoveAIToSubPath(
                material_path_str=material_structure.material_path,
            ).main()

        case "删除享设计文件夹结构的预览图":
            fun_删除享设计文件夹结构的预览图(
                material_path=Path(material_structure.material_path),
            )

        case "删除预览小图":
            fun_删除预览小图(preview_path=material_structure.preview_path)

        case "透明转白底":
            fun_透明图转白底(material_path=material_structure.material_path)

        case "PSD文件移动到子目录":
            fun_移动PSD到子目录(
                material_path=material_structure.material_path,
            )
        case "制作版权图片":
            fun_制作版权图片(
                preview_path=material_structure.preview_path,
                design_path=material_structure.design_path,
            )

    fun_通知(
        msg=f"素材ID:{Path(material_structure.material_path).name}\n{item.action}完成。",
    )

    return {"msg": "ok"}
