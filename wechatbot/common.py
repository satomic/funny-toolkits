#coding=utf-8

import requests
import datetime

def callapi(keyword):
    res = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % keyword)
    res.encoding = 'utf-8'
    ret = eval(res.text)
    # if ret.get("result") == 0:
    return ret.get("content").replace("{br}","\n")
    # return "WHAT R U F**KING SAY"

def currenttime(fmt='%Y-%m-%d %H:%M:%S'):
    return datetime.datetime.now().strftime(fmt)

def printtext(who, text):
    print("[%s] %s: %s" % (currenttime(), who, text))

def msg_content_clean(input, drain):
    return input.replace(drain, "").strip()

if __name__ == "__main__":
    print(msg_content_clean("@河边小草 你是傻逼吗","@河边小草"))