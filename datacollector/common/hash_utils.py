# coding=utf-8

import hashlib

def hash(*datas, length=32):
    data_list = []
    for data in datas:
        data_list.append(str(data))
    data_str = "!@#$%".join(data_list)
    # print(data_str)
    md5 = hashlib.md5()
    md5.update(data_str.encode('utf-8'))
    # return md5.hexdigest()[:31]
    return md5.hexdigest()[:length]



if __name__ == "__main__":
    print(hash(1,"haha",3))
    print(hash(1,"haha",3, length=31))
    print(hash(1,"haha",3, length=3))
    # print(len(hash("1-haha-3")))
