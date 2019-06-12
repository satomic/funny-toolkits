#coding=utf-8

from wxpy import *
import requests
import datetime
import platform
from queue import Queue

print("===================\n作者: 铁板豆腐\n微信: hellogitty\n===================")


# 一些函数
# ======================================================
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

# 变量初始化
# ======================================================
qr_type = 2 # default for linux
system_type = platform.system()
if(system_type == "Windows"):
    qr_type = 0

# mq = Queue()
mq = []

# 主体
# ======================================================
bot = Bot(console_qr=qr_type, cache_path ='wxpy_puid.pkl')
bot.enable_puid(path='wxpy_puid.pkl')

# 测试给小冰发送一条测试消息
xiaobin = bot.mps().search('小冰')[0]
xiaobin.send("hello! 小冰")

# 测试用所有消息
# @bot.register()
# def reply_all(msg):
#     print(msg)
#     print(msg.sender)
#     print(msg.sender.name)

debug = False

# 小冰的消息
@bot.register(bot.mps().search('小冰'))
def reply_all(msg):
    # 获取接受到小冰消息那一瞬间的时间
    current_time = currenttime(fmt='%Y-%m-%d %H:%M:%S.%f')
    input = msg.text
    printtext(msg.sender.name, input)

    if debug:
        print(mq)
    if not mq:
        if debug:
            print("[0] 队列为空")
        return
    # 如果已经有接受到的人类消息的消息队列
    elif len(mq) == 1:
        if debug:
            print("[1] 有一个元素：%s" % mq[0])
        # 如果时间迟于当前接受到消息的时间
        if mq[0].get("time") > current_time:
            return
    else:
        while (mq[0].get("time") < current_time) and (mq[1].get("time") < current_time):
            if debug:
                print("[2] 第一个元素：%s" % mq[0])
            mq.pop(0)
            if len(mq) == 1:
                break
    if debug:
        print("[3] 第一个有效元素：%s" % mq[0])

    if mq[0].get("type") == "friend":
        # mq[0].get("friend").send(input)
        msg.forward(mq[0].get("friend"))
    else:
        msg.forward(mq[0].get("group"))

# 群消息
@bot.register(bot.groups(update=True))
def reply_all(msg):

    if debug:
        print("start------------")
        print(msg)
        print(msg.type)
        print(msg.sender)
        print(msg.sender.name)
        print("stop------------")

    # 不是@的消息不回复
    if not msg.is_at:
        if msg.text == "群帮助":
            msg.reply("暖群狗会的事情如下：\n1. 新人欢迎致辞\n2. 暖群")
        # if msg.text == "群统计":
        #     msg.reply(msg.sender.members.stats())
        if "加入了群聊" in msg.text:
            msg.reply("欢迎新人~撒花~❀~~❀")
    else:
        # 获取新消息并打印
        input = msg.text[6:]
        printtext(msg.sender.name, input)
        bot.mps().search('小冰')[0].send(input)
        mq.append({
            "type": "group",
            "member": msg.member,
            "time": currenttime(fmt='%Y-%m-%d %H:%M:%S.%f'),
            "group": msg.sender,
            "msg": input,
        })

# 非群消息
@bot.register(bot.friends(update=True),except_self=False)
def reply_all(msg):

    # 非文本消息不回复
    if msg.type != TEXT:
        return

    # 获取新消息并打印
    input = msg.text
    printtext(msg.sender.name, input)
    bot.mps().search('小冰')[0].send(input)
    mq.append({
        "type": "friend",
        "time": currenttime(fmt='%Y-%m-%d %H:%M:%S.%f'),
        "friend": msg.sender,
        "msg": input,
    })
    # msg.sender.send("fuck")

embed()
