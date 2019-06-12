#coding=utf-8

import os
import sys
sys.path.append("./")
sys.path.append(".")
from sys import argv
from wxpy import *
import platform
from common import *
# from wechatbot.common import *
from ConfigLoader import Config
# from wechatbot.ConfigLoader import Config
import threading
import time

print("===================\n作者: 铁板豆腐\n微信: hellogitty\n===================")


debug = False


# 变量初始化
# ======================================================
work_dir = os.path.dirname(argv[0])
if debug:
    printtext("work_dir", work_dir)

# 加载配置
config = Config(os.path.join(work_dir, "config.json"))

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

# 测试发@
# ceshi = bot.groups().search('测试群')[0]
# ceshi.send("@%s\u2005" % "铁板豆腐")
# ceshi.send(u"@%s\u2005" % u"铁板豆腐")
# ceshi.send(r"@%s\u2005" % r"铁板豆腐")
# ceshi.send('@%s\u2005' % '铁板豆腐')
# ceshi.send(r'@%s\u2005' % r'铁板豆腐')
# ceshi.send(u'@%s\u2005' % u'铁板豆腐')
# ceshi.send(u'@铁板豆腐\u2005')
# ceshi.send(u'@铁板豆腐\u2006')
# ceshi.send("@hellogitty")
# ceshi.send('@hellogitty')
# ceshi.send(u'@hellogitty')
# ceshi.send('@' + '铁板豆腐' + '\u2005 ' )


# 测试用所有消息
# @bot.register()
# def reply_all(msg):
#     print(msg)
#     print(msg.sender)
#     print(msg.sender.name)


# 定时任务
# =========================================
class TimingJob(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("start：" + self.name)
        while True:
            if currenttime(fmt='%H:%M:%S') == config.weather.get("time"):
                xiaobin.send("上海天气")
            time.sleep(1)

timing_job = TimingJob(1, "weather_job")
timing_job.start()
# timing_job.join()

# 小冰的消息
@bot.register(bot.mps().search('小冰'))
def reply_all(msg):
    # 获取接受到小冰消息那一瞬间的时间
    current_time = currenttime(fmt='%Y-%m-%d %H:%M:%S.%f')
    input = msg.text
    printtext(msg.sender.name, input)

    # 处理天气消息
    if "上海今天的天气是" in input:
        for group_name in config.groups.keys():
            if config.groups.get(group_name).get("weather", 0) == 1:
                group = bot.groups().search(group_name)[0]
                group.send(input)

    # 其他类型
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
        print(bot.self)
        print(bot.self.name)
        print(bot.self.nick_name)
        print(bot.self.user_name)
        print(bot.self.remark_name)
        print(msg)
        print(msg.type)
        print(msg.sender)
        print(msg.sender.name)
        if u'\u2005' in msg.text:
            print("存在此字符！" + msg.text)
        print("stop------------")

    # 获取新消息并打印
    group_name = msg.sender.name
    if debug: printtext("group_name", group_name)
    group_remark_name = config.groups.get(group_name).get("group_remark_name")
    if debug: printtext("group_remark_name", group_remark_name)

    # 不是@的消息不回复
    if not msg.is_at:
        if msg.text == "群帮助":
            msg.reply("暖群狗会的事情如下：\n1. 新人欢迎致辞\n2. 每日天气提醒\n3. 暖群")
        # if msg.text == "群统计":
        #     msg.reply(msg.sender.members.stats())
        if "加入了群聊" in msg.text:
            msg.reply("欢迎新人~撒花~❀~~❀")

        if msg.text[0:4] == '@所有人':
            counter = 0
            r_msg = ""
            for member in msg.sender.members:
                if member.name == group_remark_name:
                    continue
                counter += 1
                # r_msg += u'@%s\u2005' % member.name
                r_msg += "@%s\u2005" % member.name
                # r_msg += u'@%s ' % member.name
                if counter == 50:
                    msg.reply(u'%s%s' % (r_msg, msg.text[4:]))
                    counter = 0
                    r_msg = ''
            # msg.reply(r_msg)
            msg.reply(u'%s%s' % (r_msg, msg.text[4:]))
            # if debug: printtext("bot.core", "start")
            # if debug: printtext(msg.sender.name, r_msg)
            # bot.core.send(r_msg, msg.sender.name)
            # if debug: printtext("bot.core", "stop")

    else:
        input = msg_content_clean(msg.text, "@%s" % group_remark_name)
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
