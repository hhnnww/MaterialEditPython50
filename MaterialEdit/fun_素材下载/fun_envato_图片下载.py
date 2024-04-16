from pathlib import Path
from requests_html import HTMLSession
from tqdm import tqdm


def fun_envato_图片下载(obj: dict, down_path: str):
    down_path = Path(down_path)
    if down_path.exists() is False:
        down_path.mkdir()
    img_dir = down_path / obj.get("name")

    num = 1
    while img_dir.exists() is True:
        img_dir = down_path / f"{obj.get('name')}_{num}"
        num += 1

    if img_dir.exists() is False:
        img_dir.mkdir()

    num = 1
    for img in tqdm(obj.get("img_list"), ncols=100, desc="下载envato图片"):
        img_file = img_dir / (str(num) + ".png")
        print("\n" + img_file.as_posix())
        with HTMLSession() as session:
            content = session.get("https://proxy.yumiwudesign.com/?path=" + img).content
            img_file.write_bytes(content)
            num += 1
