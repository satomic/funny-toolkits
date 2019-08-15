#coding=utf-8

import requests
import datetime
import json

def callapi(keyword):
    res = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % keyword)
    res.encoding = 'utf-8'
    ret = eval(res.text)
    # if ret.get("result") == 0:
    return ret.get("content").replace("{br}","\n")
    # return "WHAT R U F**KING SAY"

def printtext(who, text):
    print("[%s] %s: %s" % (current_time(), who, text))

def msg_content_clean(input, drain):
    return input.replace(drain, "").strip()

def current_time(fmt='%Y-%m-%d %H:%M:%S.%f'):
    return datetime.datetime.now().strftime(fmt)[:-3]


def print_base(base_info, type):
    print("%s [%s] %s" % (current_time(), type, base_info))


def print_err(err, type="ERRO"):
    print_base(err, type)


def print_info(info, type="INFO"):
    print_base(info, type)


def print_warn(warn, type="WARN"):
    print_base(warn, type)

def gen_json_str(j, quot='"'):
    return str(j).replace("'", '"')

def get_json_formated(j):
    return json.dumps(j, indent=2)

if __name__ == "__main__":
    print(msg_content_clean("@河边小草 你是傻逼吗","@河边小草"))
    test = {1:1,2:2}
    print(test.keys())
    print("07:00:00"[0:5])
    print(gen_json_str({"haha":123}))