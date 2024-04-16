def fun_构建链接列表(base_url: str, start_num: int, end_num: int):
    for x in range(start_num, end_num):
        yield base_url.replace("*", str(x))
