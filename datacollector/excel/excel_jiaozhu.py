# coding=utf-8

import os
import sys
sys.path.append("../..")
# from os.path import abspath, join, dirname
# sys.path.insert(0, abspath(dirname(__file__)))

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

    cursor = 1

    def __init__(self, sheet_name,
                 row_index_battle=1,
                 row_indexs_battle_zone=[2,3,4,5],
                 col_index_zone="A",
                 col_index_battle_zone="B",
                 col_index_gmv="C",
                 col_index_ago_long="D",
                 col_index_ago="E",
                 col_index_now="F"):
        self.sheet_name = sheet_name
        self.row_index_battle = row_index_battle - self.cursor
        self.row_indexs_battle_zone = list(map(lambda i: i - self.cursor, row_indexs_battle_zone))
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
                 row_index_battle=1,
                 row_indexs_battle_zone=[2,3,4,5],
                 col_index_zone="A",
                 col_index_battle_zone="B",
                 col_index_gmv="C",
                 col_index_ago_long="D",
                 col_index_ago="E",
                 col_index_now="F"):

        if not file_utils.is_specify_type_file(xlsx_file, ["xlsx", "xls"]):
            common.print_err("falal error!")

        self.sheet_structure = SheetStructure(sheet_name=sheet_name,
                                              row_index_battle=row_index_battle,
                                              row_indexs_battle_zone=row_indexs_battle_zone,
                                              col_index_zone=col_index_zone,
                                              col_index_battle_zone=col_index_battle_zone,
                                              col_index_gmv=col_index_gmv,
                                              col_index_ago_long=col_index_ago_long,
                                              col_index_ago=col_index_ago,
                                              col_index_now=col_index_now)
        self.sheet = Sheet(xlsx_file, self.sheet_structure.sheet_name)

    def get_city_list(self):
        row_range = range(self.sheet.get_row_number())
        print(row_range)









if __name__ == "__main__":
    excel = r"D:\workspace\funny-toolkits\datacollector\samples\data_sample_1.xlsx"
    one_data = OneData(excel, 0)
    one_data.get_city_list()


