from pathlib import Path

import keyboard


def move_envato_file():
    down_path = Path(r"F:\\DOWN")
    fantong_path = Path(r"F:\\DOWN\\可制作\\饭桶")

    new_path = fantong_path / "新建文件夹"
    i = 1
    while new_path.exists():
        new_path = fantong_path / f"新建文件夹 ({i})"
        i += 1

    for in_file in down_path.iterdir():
        if in_file.suffix in [".zip", ".jpg", ".png"] and in_file.is_file():
            if new_path.exists() is not True:
                new_path.mkdir()

            sc_new_file_path = new_path / in_file.name
            in_file.rename(sc_new_file_path)


print("正在运行，自动移动素材程序。快捷键 alt+b")
keyboard.add_hotkey("alt+b", move_envato_file)
keyboard.wait("esc")
