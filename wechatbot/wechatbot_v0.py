#coding=utf-8

from wxpy import *
import requests
import datetime
import platform

def callapi(keyword):
    res = requests.get('http://api.qingyunke.com/api.php?key=free&appid=0&msg=%s' % keyword)
    res.encoding = 'utf-8'
    ret = eval(res.text)
    # if ret.get("result") == 0:
    return ret.get("content").replace("{br}","\n")
    # return "WHAT R U F**KING SAY"

def currenttime():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def printtext(who, text):
    print("[%s] %s: %s" % (currenttime(), who, text))

qr_type = 2 # default for linux
system_type = platform.system()
if(system_type == "Windows"):
    qr_type = 0

# bot = Bot(console_qr=2)
bot = Bot(console_qr=qr_type, cache_path ='wxpy_puid.pkl')
bot.enable_puid(path='wxpy_puid.pkl')

print("===================\n作者: 铁板豆腐\n微信: hellogitty\n说明: 调用的免费APIhttp://api.qingyunke.com/api.php?key=free&appid=0&msg=你好，所以可能会请求失败\n===================")

@bot.register()
def reply_all(msg):
    if msg.type != TEXT:
        return
    if msg.member is not None and not msg.is_at:
        return
    input = msg.text
    printtext(msg.sender.name, input)

    output = callapi(input)

    printtext("河边小草", output)
    msg.reply(output)

embed()
