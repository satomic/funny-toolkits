# coding=utf-8

from excel.excel_jiaozhu import OneData
import common.file_utils as file_utils
import common.common as common

class City(object):

    def __init__(self, battle_zone, gmv, power_ago_long, power_ago, power_now):
        self.battle_zone = battle_zone
        self.gmv = gmv
        self.power_ago_long = power_ago_long
        self.power_ago = power_ago
        self.power_now = power_now


class Result(object):

    def __init__(self):
        self.citys = {}
        self.battle_zones = {}
        self.total = {}


gmv_str = "GMV"
battle_zone_str = "battle_zone"
subsidy_str = "subsidy"


needed_date_ago_long = "201907力度"
needed_date_ago = "201908力度"
needed_date = "201909力度"

titles_std = ["区域", "归属战区", gmv_str, needed_date_ago_long, needed_date_ago, needed_date]


excel_path = r"D:\workspace\funny-toolkits\datacollector\samples\simudata"
excels = file_utils.get_all_files(excel_path)

result = Result()

# 对于每一个excel遍历一遍
for excel in excels:

    # 读取当前excel内容，读取第一个sheet页，默认应该是项目名称，此处不做判断，直接取值
    one_data = OneData(excel, 0)

    # 检查一下格式是否合法
    titles = one_data.sheet.row_values(0)
    if titles[:3] != titles_std[:3]:
        common.print_err("excel:%s的title栏前3列无效" % excel)
        continue

    # 如果时间不符合当前需求，直接跳过
    if one_data.get_now_date() != needed_date:
        common.print_warn("excel:%s不是当前所关注的时间点" % excel)
        continue

    if titles[3:5] != titles_std[3:5]:
        common.print_err("excel:%s的过去时间与当前时间不匹配" % excel)
        continue

    # 获取项目名称
    project_name = one_data.sheet_names[0]

    # 获取详细信息，并遍历
    citys, errs = one_data.get_city_datas()
    for err in errs:
        common.print_err("在excel:%s中有错误信息:%s" % (excel, err))
    for city, info in citys.items():

        # 以城市为维度进行数据统计
        # 如果城市是第一次出现
        if city not in result.citys.keys():
            # 初始化城市数据
            result.citys[city] = {
                gmv_str: info.get(gmv_str),
                battle_zone_str: info.get("归属战区"),
                needed_date: 0,
                "projects": {}
            }

        # 额外存储以项目维度的数据方便未来扩展
        power_now = info.get(needed_date)
        result.citys[city]["projects"][project_name] = power_now
        result.citys[city][needed_date] += power_now

# 计算战区
# 补贴金额，逐个城市计算
for city,info in result.citys.items():
    gmv = info.get(gmv_str)
    power = info.get(needed_date)

    # 计算出一个城市的所有补贴
    subsidy = gmv * power
    result.citys[city][subsidy_str] = subsidy

    battle_zone = info.get(battle_zone_str)

    # 初始化城市数据
    if battle_zone not in result.battle_zones.keys():
        result.battle_zones[battle_zone] = {
            subsidy_str: 0,
            gmv_str: 0,
            needed_date: 0,
            "citys": {}
        }
    # 补贴累加
    result.battle_zones[battle_zone][subsidy_str] += subsidy
    result.battle_zones[battle_zone][gmv_str] += gmv



# 都计算完了除一下
for battle_zone, info in result.battle_zones.items():
    result.battle_zones[battle_zone][needed_date] = info[subsidy_str] / info[gmv_str]

    # 计算全国
    if not result.total:
        result.total = {
            subsidy_str: 0,
            gmv_str: 0,
            needed_date: 0
        }
    result.total[subsidy_str] += info[subsidy_str]
    result.total[gmv_str] += info[gmv_str]

#  最终计算一下全国的
result.total[needed_date] = result.total[subsidy_str] / result.total[gmv_str]


# 打印关键数据
# 全国数据
if True:
    print("全国的力度")
    info = result.total
    print("全国: %s=%s, %s=%s, %s=%s" % (needed_date, info.get(needed_date), subsidy_str, info.get(subsidy_str), gmv_str, info.get(gmv_str)))
    print("------------------------------------------")
    print("战区的力度")
    for battle_zone, info in result.battle_zones.items():
        print("%s: %s=%s, %s=%s, %s=%s" % (battle_zone, needed_date, info.get(needed_date), subsidy_str, info.get(subsidy_str), gmv_str, info.get(gmv_str)))
    print("------------------------------------------")
    print("城市的力度")
    for city, info in result.citys.items():
        print("%s: %s=%s, %s=%s, %s=%s" % (city, needed_date, info.get(needed_date), subsidy_str, info.get(subsidy_str), gmv_str, info.get(gmv_str)))



csv_contents = []
csv_contents.append("范围,战区,力度,补贴,GMV")
info = result.total
csv_contents.append("%s,%s,%s,%s,%s" % ("全国", "", info.get(needed_date), info.get(subsidy_str), info.get(gmv_str)))
for battle_zone, info in result.battle_zones.items():
    csv_contents.append("%s,%s,%s,%s,%s" % (battle_zone, "", info.get(needed_date), info.get(subsidy_str), info.get(gmv_str)))
for city, info in result.citys.items():
    csv_contents.append("%s,%s,%s,%s,%s" % (city, info.get(battle_zone_str), info.get(needed_date), info.get(subsidy_str), info.get(gmv_str)))

csv_contents = "\n".join(csv_contents)
with open("result_%s.csv" % common.current_time(fmt='%Y%m%d_%H%M%S%f'), "w") as f:
    f.write(csv_contents)