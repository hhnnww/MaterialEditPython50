from pathlib import Path

from PIL import Image


def fun_蜘蛛水印(im: Image.Image):
    water_path = Path(__file__).parent / "蜘蛛水印.png"
    water_pil = Image.open(water_path.as_posix())
    im.thumbnail((1500, 99999))
    top = 0
    bottom = water_pil.height
    left = int((im.width - water_pil.width) / 2)
    while bottom < im.height:
        im.paste(water_pil, (left, top), water_pil)

        top += water_pil.height
        bottom += water_pil.height

    return im


if __name__ == "__main__":
    from pathlib import Path

    hs_up = Path(r"\\HUANGSHUO\Users\materialedit\Desktop\UPLOAD")
    ma_path = Path(r"F:\小夕素材\10000-20000\10587\10587")
    for in_file in ma_path.rglob("*"):
        if in_file.is_file() and in_file.suffix.lower() in [".png", ".jpg"]:
            print(in_file)

            if in_file.parent.stem.lower() == "links":
                print(f"{in_file} 跳过")
                continue

            im = Image.open(in_file.as_posix())
            im = fun_蜘蛛水印(im=im)
            im.save(in_file.as_posix())
