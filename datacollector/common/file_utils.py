# coding=utf-8

import os
import common.common as common
import shutil

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

def get_all_files(file_dir, ext=[]):
    # ext=[".xls", ".xlsx"]
    """
    :param file_dir: 
    :return: 递归获取所有文件完整路径 
    """
    ret = []
    for root, dirs, files in os.walk(file_dir):
        # print("------------------------------")
        # print('root_dir:', root)  # 当前目录路径
        # print('sub_dirs:', dirs)  # 当前路径下所有子目录
        # print('files:', files)  # 当前路径下所有非目录子文件
        if ext:
            files = list(filter(lambda file: os.path.splitext(file)[-1] in ext, files))
        files = list(map(lambda file: os.path.join(root, file), files))
        ret.extend(files)
    return ret

def replace_filename(filename_old, filename_new, dir_new=""):
    dirname = os.path.dirname(filename_old)
    basename = os.path.basename(filename_old)
    filename, extname = os.path.splitext(basename)
    if dir_new:
        dirname = dir_new
    return os.path.join(dirname, "%s%s" % (filename_new, extname))

def copy_file(file_src, file_dst):
    shutil.copy(file_src, file_dst)

def move_file(file_src, file_dst):
    shutil.move(file_src, file_dst)

if __name__ == "__main__":
    # print(is_specify_type_file("common.py",["PY","haha"]))
    # files = get_all_files(r"D:\workspace\funny-toolkits\datacollector")
    # for file in files:
    #     print(file)

    replace_filename(r"D:\workspace\funny-toolkits\datacollector\uploads\data_sample_3.xlsx", "haha")
    file = r"D:\workspace\funny-toolkits\datacollector\uploads\data_sample_3.xlsx"
    print(replace_filename(file, "haha", dir_new="123123"))
