def fun_构建header(header: str) -> dict:
    header_dict = {}
    for line in header.split("\n"):
        if ": " in line:
            line_split = line.split(": ")
            header_dict[line_split[0]] = line_split[1]

    return header_dict
