# coding=utf-8

import sys
sys.path.append("./")
sys.path.append(".")
import requests
from bs4 import BeautifulSoup
import threading
import time
import datetime
import os
import wechatbot.common as common


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'Cookie': 'TY_SESSION_ID=73a14e97-b703-4777-bc59-25f8999619f0; lianjia_uuid=6aaa8715-f71d-4217-a09b-3acae61b4112; _smt_uid=5c7a3c88.5b4cce3c; UM_distinctid=1693d7c76fe1e5-036c807be77add-b781636-144000-1693d7c76ff25f; _ga=GA1.2.1846587678.1551514765; Hm_lvt_8875c662941dbf07e39c556c8d97615f=1553434645; lianjia_token=2.001d88abe564facfbd0c2582d412e47dca; _jzqy=1.1554619222.1554619222.1.jzqsr=baidu.-; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22169b9cf56c2f0-090d5b4109481d-b781636-1327104-169b9cf56c3335%22%2C%22%24device_id%22%3A%22169b9cf56c2f0-090d5b4109481d-b781636-1327104-169b9cf56c3335%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _jzqx=1.1558090305.1560612577.3.jzqsr=sh%2Elianjia%2Ecom|jzqct=/ditu/.jzqsr=sh%2Elianjia%2Ecom|jzqct=/ershoufang/rs%e9%be%99%e5%b7%9e%e5%b0%8f%e5%8c%ba/; all-lj=c60bf575348a3bc08fb27ee73be8c666; select_city=310000; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1560567357,1560700642,1560915850,1561192043; _qzjc=1; _jzqc=1; _jzqckmp=1; _gid=GA1.2.965185712.1561192047; Hm_lvt_efa595b768cc9dc7d7f9823368e795f1=1560567337,1560700570,1561192103; lianjia_ssid=973ddfb0-def9-4a58-be2f-e6a211524bf8; CNZZDATA1253492439=741343867-1551511076-%7C1561206345; CNZZDATA1255633284=907477815-1551513116-%7C1561207032; _jzqa=1.3651648014459960000.1551514761.1561192044.1561210116.18; Hm_lpvt_efa595b768cc9dc7d7f9823368e795f1=1561210139; CNZZDATA1255604082=1206902743-1551511039-%7C1561210607; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1561211485; CNZZDATA1254525948=1577455821-1551512960-%7C1561211176; _qzja=1.588207922.1551514762650.1561192043733.1561210115575.1561211126623.1561211485581.0.0.0.660.18; _qzjb=1.1561210115575.19.0.0.0; _qzjto=41.2.0; _jzqb=1.19.10.1561210116.1; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiZjI0ZDYzNDdlY2YzZGY4ZTNkOGI0YzY0YzJhZmQ0MjBlN2I2Njc1NGUyNGFiNGIzODc2N2FiMmY5YmZlMjIyYTI4ZWY2ZWVkMmViM2EwYzUyY2ZmNGE5YTY1OWIxYTQwMjNiNGMxNDI1MDlkOThiY2ExMzhkODQxMTM5NGE0YTY2MGFkNWMyZTE1NzI4MDJkNjdlNjJlZTBmMTBmYWU1YWJlMTU1MGYxMmE5YTJhZmUzY2Y5OTdjMmQyOGE0OTI5YzU4MTA2OGYxMDViODI0NmM4ZDg2YTkyNGYyZTMzNzI1MDUwOTEwZWEyZDdkMWMzN2M1NzhmYzZjMTc2ZjhiYzFlM2ZmYmQ2MjdiOWMwYjM0ZjkyYTI0NTlhZDY1ZmY5ZDM3ZjEzMzY2NzM0NmQxZGViYzk2NWMzMzljYzUxZjdkMzkwYjgyNzAzNzY5YjgwNGQ3OGI4YTUyOWEwMWE1YlwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCIzMTVkZjIzYlwifSIsInIiOiJodHRwczovL3NoLmxpYW5qaWEuY29tL2Vyc2hvdWZhbmcvMTA3MTAwNDY4OTAzLmh0bWwiLCJvcyI6IndlYiIsInYiOiIwLjEifQ==',
}


def request_lianjia(hash="de2de1lc1lc2l2l3a2a3bp250ep340"):
    url = "https://sh.lianjia.com/ershoufang/huadongligong/%s/" % hash
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return parse_result(response.text)
    except requests.RequestException:
        return None

def parse_result(html):
    soup = BeautifulSoup(html, 'lxml')
    bigImg = soup.findAll("div", {"class": "bigImgList"})[0]

    ret = []
    items = bigImg.findAll("div", {"class": "item"})
    for item in items:

        data = {}
        a_img = item.findAll("a", {"class": "img"})[0]
        data["href"] = a_img["href"]
        data["housecode"] = a_img["data-housecode"]

        data["price"] = a_img.findAll("div", {"class": "price"})[0].get_text()
        a_title = item.findAll("a", {"class": "title"})[0]
        data["desc"] = a_title.string

        data["info"] = item.findAll("div", {"class": "info"})[0].get_text()

        ret.append(data)
    return ret


# 定时任务
# =========================================

class DataLocal():

    def __init__(self, data_path="data.txt"):
        self.data_path = data_path
        if not os.path.exists(self.data_path):
            common.print_warn("%s is not exists, so create it" % self.data_path)
            with open(self.data_path, "w", encoding="UTF-8") as f:
                f.write("")
        self.housecodes = []
        common.print_info("load data local started")
        with open(self.data_path, "r", encoding="UTF-8") as f:
            for line in f.readlines():
                self.housecodes.append(line.strip())
        common.print_info("local data local successfully, %s" % self.housecodes)

    def has_code(self, code):
        return code in self.housecodes

    def add_code(self, code):
        self.housecodes.append(code)
        with open(self.data_path, "a", encoding="UTF-8") as f:
            f.write("%s\n" % code)
        common.print_info("a new house added to data local successfully: https://sh.lianjia.com/ershoufang/%s.html" % code)


class TimingJobLianjia(threading.Thread):

    def __init__(self, threadID, name, bot):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.data_local = DataLocal()
        self.bot = bot

    def run(self):
        print("start：" + self.name)
        while True:
            datas = request_lianjia(hash="de2de1lc1lc2l2l3a2a3bp250ep340")
            for data in datas:
                code = data.get("housecode")
                if self.data_local.has_code(code):
                    continue
                common.print_info("a new house will be added to data local: %s" % data)
                self.data_local.add_code(code)
                info = "标题：%s\n价格：%s\n详情：%s\n链接：%s" % (data.get("desc"), data.get("price"), data.get("info"), data.get("href"))
                self.bot.send(info)
            time.sleep(300)

if __name__ == "__main__":
    datas = request_lianjia(hash="de2de1lc1lc2l2l3a2a3bp250ep340")
    print("len: %s" % len(datas))
    for data in datas:
        print(data)

    # timing_job = TimingJobLianjia(1, "alerting for new house")
    # timing_job.start()