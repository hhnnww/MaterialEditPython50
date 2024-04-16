from ...type import _FontSize


def fun_计算一行文字的宽度和高度(font_size_list: list[_FontSize]) -> _FontSize:
    height = max([obj.height for obj in font_size_list])
    width = sum([obj.width for obj in font_size_list])
    return _FontSize(width=width, height=height)
