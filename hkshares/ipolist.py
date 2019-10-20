# coding=utf-8

import requests
from bs4 import BeautifulSoup
import threading
import time
import datetime
import os
import common as common
import traceback

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}

def request_ipolist(url="http://vip.stock.finance.sina.com.cn/q/view/hk_IPOList.php"):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            ret = parse_result(response.text.encode("latin1").decode("GBK"))
            return ret
    except requests.RequestException:
        return None
    except Exception as e:
        common.print_err(traceback.format_exc(e))
        return None

def parse_result(html):
    soup = BeautifulSoup(html, 'lxml')
    ipolist_table = soup.findAll("div", {"class": "content"})[0]

    ret = []
    items = ipolist_table.findAll("tbody")[0].findAll("tr")
    for item in items:
        """
		<td><a href="./hk_IPOProfile.php?symbol=01871" target="_blank">01871</a></td>
		<td><a href="./hk_IPOProfile.php?symbol=01871" target="_blank">向中国际控股有限公司</a></td>
		<td>1.42-1.28		</td>
		<th>100000000</th>
		<th>0.00</th>
		<td>2019-10-11至2019-10-16		</td>
		<td>2019-10-24</td>
		<td id="price_01871">--</td>
		<td id="change_01871">--</td>
		<td id="chgrate_01871">--</td>
        """
        elements_type1 = item.findAll("td")
        elements_type2 = item.findAll("th")
        element = {
            "code" : elements_type1[0].get_text().strip(),
            "name" : elements_type1[1].get_text().strip(),
            "price" : elements_type1[2].get_text().strip(),
            "quantity" : elements_type2[0].get_text().strip(),
            "got_money" : elements_type2[1].get_text().strip(),
            "date_of_offering_begin" : elements_type1[3].get_text().strip().split("至")[0],
            "date_of_offering_end": elements_type1[3].get_text().strip().split("至")[-1],
            "date_of_listing" : elements_type1[4].get_text().strip()
        }
        ret.append(element)
        # print(element)
    return ret




# 定时任务
# =========================================

class TimingJob(threading.Thread):

    def __init__(self, name, time_list = [], bot=None):
        threading.Thread.__init__(self)
        self.name = name
        self.time_list = time_list
        self.time_index_for_next_task = None
        if self.time_list:
            self.time_index_for_next_task = 0
        self.bot = bot

    def get_next_time_index(self):
        total_time_number = len(self.time_list)
        self.time_index_for_next_task += 1
        if self.time_index_for_next_task == total_time_number:
            self.time_index_for_next_task = 0

    def run(self):
        print("start：" + self.name)
        while True:
            if self.time_index_for_next_task is None:
                self.task()
            else:
                # 获取当前时间与日期比对
                current_time = common.current_time(fmt='%H:%M')
                # current_time = "00:32"
                if current_time == self.time_list[self.time_index_for_next_task]:
                    self.task()
                    self.get_next_time_index()
            time.sleep(5)

    def task(self):
        datas = request_ipolist()
        # datas = request_ipolist(url="http://47.75.216.239:8080/demo.html")
        if datas:
            current_date = common.current_time(fmt='%Y-%m-%d')
            common.print_info("---------------当前日期: %s---------------" % current_date)
            info = ""
            for data in datas:
                # 招股
                date_of_offering_begin = data.get("date_of_offering_begin")
                date_of_offering_end = data.get("date_of_offering_end")
                if (date_of_offering_begin <= current_date) & (current_date <= date_of_offering_end):
                    info += "---新股招股---\n日期: %s至%s\n代码: %s\n价格: %s\n名称: %s\n\n" % \
                          (date_of_offering_begin,
                          date_of_offering_end,
                          data.get("code"),
                          data.get("price"),
                          data.get("name"))
                    common.print_info(info)
                # 暗盘
                date_of_listing = data.get("date_of_listing")
                date_dark_pools = common.date_add_day(date_of_listing, -1)
                if date_dark_pools == current_date:
                    info += "---今日暗盘---\n日期: %s 04:15PM\n代码: %s\n价格: %s\n名称: %s" % \
                          (date_dark_pools,
                          data.get("code"),
                          data.get("price"),
                          data.get("name"))
                    common.print_info(info)
            if info:
                self.bot.send(info)

if __name__ == "__main__":
    # request_ipolist()
    # job = TimingJob("new shares", time_list=["00:39", "00:40","09:00","10:00"])
    job = TimingJob("new shares", time_list=[])
    job.run()
    # print(common.current_time(fmt='%Y-%m-%d %H'))