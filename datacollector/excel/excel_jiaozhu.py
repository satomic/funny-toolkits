# coding=utf-8

import os
import sys
sys.path.append("../..")
# from os.path import abspath, join, dirname
# sys.path.insert(0, abspath(dirname(__file__)))
import numpy as np
from excel.excel_utils import Sheet
import common.file_utils as file_utils
import common.common as common


class SheetStructure():

    index_mapping = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
    }

    zone = "区域"

    cursor = 1

    def __init__(self, sheet_name,
                 row_index_header=1,
                 row_index_battle_zone=[2,3,4,5],
                 col_index_zone="A",
                 col_index_battle_zone="B",
                 col_index_gmv="C",
                 col_index_ago_long="D",
                 col_index_ago="E",
                 col_index_now="F"):
        self.sheet_name = sheet_name
        self.row_index_header = row_index_header - self.cursor
        self.row_index_battle_zone = list(map(lambda i: i - self.cursor, row_index_battle_zone))
        self.col_index_zone = self.mapping_index_str_2_int(col_index_zone)
        self.col_index_battle_zone = self.mapping_index_str_2_int(col_index_battle_zone)
        self.col_index_gmv = self.mapping_index_str_2_int(col_index_gmv)
        self.col_index_ago_long = self.mapping_index_str_2_int(col_index_ago_long)
        self.col_index_ago = self.mapping_index_str_2_int(col_index_ago)
        self.col_index_now = self.mapping_index_str_2_int(col_index_now)

    def mapping_index_str_2_int(self, index_str):
        if index_str not in self.index_mapping.keys():
            return -1
        return self.index_mapping.get(index_str.upper())


class OneData():

    def __init__(self,
                 xlsx_file,
                 sheet_name,
                 row_index_header=1,
                 row_index_battle_zone=[2,3,4,5],
                 col_index_zone="A",
                 col_index_battle_zone="B",
                 col_index_gmv="C",
                 col_index_ago_long="D",
                 col_index_ago="E",
                 col_index_now="F"):

        if not file_utils.is_specify_type_file(xlsx_file, ["xlsx", "xls"]):
            common.print_err("falal error!")

        self.sheet_structure = SheetStructure(sheet_name=sheet_name,
                                              row_index_header=row_index_header,
                                              row_index_battle_zone=row_index_battle_zone,
                                              col_index_zone=col_index_zone,
                                              col_index_battle_zone=col_index_battle_zone,
                                              col_index_gmv=col_index_gmv,
                                              col_index_ago_long=col_index_ago_long,
                                              col_index_ago=col_index_ago,
                                              col_index_now=col_index_now)
        self.sheet = Sheet(xlsx_file, self.sheet_structure.sheet_name)

    def get_city_row_indexs(self):
        # print(self.sheet_structure.row_index_header)
        # print(self.sheet_structure.col_index_battle_zone)
        index_others = [self.sheet_structure.row_index_header] + self.sheet_structure.row_index_battle_zone
        # print(index_others)
        return list(filter(lambda i: i not in index_others, self.sheet.row_index_range))

    def get_city_list(self):
        zone_list = np.array(self.sheet.col_values(self.sheet_structure.col_index_zone))
        return list(zone_list[self.get_city_row_indexs()])

    def get_city_datas(self):
        """
        :return: 只要err的返回不为空，那么就要求修改数据直到通过为止
        """
        city_datas = {}
        err_city_datas = []
        for index in self.get_city_row_indexs():
            row_dict = self.sheet.get_row_dict_with_header(index, index_header=self.sheet_structure.row_index_header,cursor=0)
            city = row_dict.pop(self.sheet_structure.zone)
            bad_city_data = self.check_city_validity(row_dict)
            if bad_city_data:
                err_city_datas.append({city: bad_city_data})
            else:
                city_datas[city] = row_dict
        return city_datas, err_city_datas

    def check_city_validity(self, city_info):
        # todo 每个字段的有效性检查
        # todo 当前月份数据基于之前数据的验证
        """
        :param city_info: 城市信息字典 
        :return: 异常城市为key的包含异常字段的字典list
        """
        return []








if __name__ == "__main__":
    excel = r"D:\workspace\funny-toolkits\datacollector\samples\data_sample_1.xlsx"
    one_data = OneData(excel, "项目1")
    # print(one_data.get_city_datas())
    citys,errs = one_data.get_city_datas()
    for city,info in citys.items():
        print(city, info)
    print(errs)

