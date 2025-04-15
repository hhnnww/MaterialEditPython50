"""把一长段文字换行"""

import textwrap


def fun_文字换行(text: str, line_max_number: int) -> list[str]:
    """把一长段文字换行

    Returns:
        _type_: _description_

    """
    return textwrap.fill(text=text, width=line_max_number).split("\n")


if __name__ == "__main__":
    print(
        fun_文字换行(
            text="""模块可用于在需要漂亮打印的情况下格式化输出文本。它提供的编程功能类似于许多文本编辑器和文字处理器中的段落包装或填充功能。""",
            line_max_number=10,
        ),
    )
