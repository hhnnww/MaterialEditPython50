import string


def fun_是英文(text: str) -> bool:
    if len(text) > 1:
        raise IndexError("只能传入一个字符")

    return text in string.ascii_letters + string.digits


if __name__ == "__main__":
    print(string.ascii_letters + string.digits)
