# coding=utf-8

import os
import common as common

def is_exist(file):
    if not os.path.exists(file):
        common.print_warn("%s is not exist" % file)
        return False
    return True

def is_specify_type_file(file, ext_wanna_list):
    if isinstance(ext_wanna_list, str):
        ext_wanna_list = [ext_wanna_list]

    # 加上点，同时弄成小写的
    ext_wanna_list = list(map(lambda e: (".%s" % e).lower() if e[0] != "." else e.lower(), ext_wanna_list))
    if not is_exist(file):
        return False
    filename, ext_real = os.path.splitext(file)
    if ext_real not in ext_wanna_list:
        common.print_warn("%s's extension is not wanted file type" % file)
        return False
    return True


if __name__ == "__main__":
    print(is_specify_type_file("common.py",["PY","haha"]))

