#coding=utf-8

import requests
import datetime

def callapi(keyword):
    res = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % keyword)
    res.encoding = 'utf-8'
    ret = eval(res.text)
    if ret.get("result") == 0:
        return ret.get("content")
    return "WHAT R U F**KING SAY"

def currenttime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    print("@河边小草 你是傻逼吗"[6:])