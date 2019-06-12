#coding=utf-8

from wxpy import *
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

def printtext(who, text):
    print("[%s] %s: %s" % (currenttime(), who, text))

# bot = Bot(console_qr=0)
bot = Bot(console_qr=2, cache_path ='wxpy_puid.pkl')
bot.enable_puid(path='wxpy_puid.pkl')

@bot.register()
def reply_all(msg):
    if msg.type != TEXT:
        return
    if msg.member is not None and not msg.is_at:
        return
    input = msg.text
    printtext(msg.sender.name, input)
    output = callapi(input).replace("{br}","\n")
    printtext("河边小草", output)
    msg.reply(output)

embed()

