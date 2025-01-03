"""解压ZIP文件"""

import subprocess
from pathlib import Path


def fun_unzip_file(file_path: Path) -> None:
    """解压zip文件"""
    subprocess.Popen(
        args=[
            "C:\\Program Files\\Bandizip\\Bandizip.exe",
            "x",
            "-target:name",
            file_path.as_posix(),
        ],
    )
