# coding=utf-8

import os
import sys
sys.path.append("./")
sys.path.append(".")
from sys import argv
from wxpy import *
import platform
import common as common
# from wechatbot.ConfigLoader import Config
import threading
import time
from ipolist import TimingJob

print("===================\n作者: 铁板豆腐\n微信: hellogitty\n===================")


debug = True
debug = False


# 变量初始化
# ======================================================
work_dir = os.path.dirname(argv[0])
common.print_info("work_dir", work_dir)

# 加载配置
# config = Config(os.path.join(work_dir, "config.json"))
# common.print_info("config.weather: %s" % config.weather)

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

# 发送一条测试消息
xiaobin = bot.friends().search('铁板豆腐')[0]
xiaobin.send("hello! 铁板豆腐")


tofu = bot.groups().search('港股打新提醒')[0]
timing_job_ipo = TimingJob("new shares", time_list=["08:00", "11:40", "16:00"], bot=tofu)
timing_job_ipo.start()


embed()
