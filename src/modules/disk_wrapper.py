import os


def write_file(file_path, content, mode="w"):
    try:
        file = open(file_path, mode)
        file.write(content)
    except FileNotFoundError:
        os.makedirs("/".join(file_path.split("/")[:-1]))
        write_file(file_path, content, mode)


def read_file(file_path, mode="r"):
    file = open(file_path, mode)
    return file.read()
