# coding=utf-8

import os
import xlrd
from datetime import datetime
import traceback
from xlutils.copy import copy
import shutil
import openpyxl # 需要升级到最新的2.6.2版本 python -m pip install --upgrade openpyxl


class Excel(object):

    def __init__(self, excel_file):
        self.excel = xlrd.open_workbook(excel_file)
        self.sheet_names = self.excel.sheet_names()

    def get_sheet(self, sheet_name=0):
        """
        :param sheet_name: identify a sheet by a index/name
        :return: sheet object
        """
        try:
            if isinstance(sheet_name, int):
                return self.excel.sheet_by_index(sheet_name)
            if isinstance(sheet_name, str):
                if sheet_name in self.sheet_names:
                    return self.excel.sheet_by_name(sheet_name)
                else:
                    print("sheet name: %s does not exist in excel file" % (sheet_name))
        except Exception as e:
            print(traceback.format_exc(e))
            return None

def find_left_index(iter, value):
    for i in range(len(iter)-1):
        if iter[i] <= value and iter[i+1] > value:
            # print iter[i], iter[i+1]
            return i
    return -1

def find_all_index(iter, value, cursor=0):
    ret = []
    for i in range(len(iter)):
        if iter[i] == value:
            ret.append(i + cursor)
    return ret

def get_intersection(l1, l2):
    if l1 == -1 or l2 == -1:
        return -1
    difference = list(set(l1).intersection(set(l2)))
    if len(difference) == 0:
        return -1
    elif len(difference) == 1:
        return difference[0]
    else:
        raise Exception("multi row indexs are got, this is illegal")


def copy_file(file_old, file_new_prefix):
    str_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    str_new = '{0}_{1}.xlsx'.format(file_new_prefix, str_time)
    shutil.copyfile(file_old, str_new)
    return str_new


class Sheet(object):

    def __init__(self, excel, sheet_name):
        excel = excel.replace("\\","/")
        if isinstance(excel, str):
            if os.path.exists(excel):
                excel = Excel(excel)
            else:
                raise Exception("excel file: %s is not exists" % excel)
        self.sheet = excel.get_sheet(sheet_name)

    def row_values(self, index):
        return self.sheet.row_values(index)

    def col_values(self, index):
        return self.sheet.col_values(index)

    def get_row_number(self):
        return len(self.col_values(0))

    def get_col_number(self):
        return len(self.row_values(0))

    def get_col_index_by_value(self, value, key_row_index=0, cursor=4):
        row_values = self.sheet.row_values(key_row_index)[cursor:]
        return find_left_index(row_values, value) + cursor
        # if value not in row_values:
        #     return -1
        #     raise Exception("value: %s does not in the key row" % value)
        # return row_values.index(value)

    def get_row_index_by_value(self, value, key_col_index=0, cursor=3):
        col_values =  self.sheet.col_values(key_col_index)[cursor:]

        # print len(col_values),col_values
        # print value

        if value not in col_values:
            return -1
            raise Exception("value: %s does not in the key col" % value)
        # return col_values.index(value) + cursor
        return find_all_index(col_values, value, cursor)

class Updater(object):

    def __init__(self, excel_file, on_origin=True):
        wb = xlrd.open_workbook(excel_file)
        if on_origin:
            self.excel = wb
        else:
            self.excel = copy(wb)
        self.sheet = None

    def set_sheet(self, sheet_index):
        self.sheet = self.excel.get_sheet(sheet_index)

    def update(self, row, col, value):
        self.sheet.write(row, col, value)

    def save(self, file_name):
        self.excel.save(r"%s.xls" % file_name)



if __name__ == "__main__":

    # cool test
    # original_excel = "data_sample.xlsx"
    # final_sheet_tamplate_file = "tamplate.xlsx"
    #
    # # load original data
    # original_sheet = Sheet(original_excel, "原始")
    # gongxian_danliang = original_sheet.col_values(1)
    # print("load orignal data: %s" % gongxian_danliang)
    #
    # # save to a tamplate file
    # updater =openpyxl.load_workbook(final_sheet_tamplate_file)
    # sheet = updater.get_sheet_by_name('结果')
    # row_counter = 2
    # for value in gongxian_danliang[1:]: # 排除掉第一个title
    #     sheet.cell(row=row_counter, column=2, value=value) # 自然计数，从1开始算
    #     row_counter += 1
    #
    # report_name = "result_%s.xlsx" % datetime.now().strftime('%Y%m%d_%H%M%S')
    # updater.save(report_name)
    # print("report generated: %s" % report_name)

    original_excel = "data_sample.xlsx"

    # load original data
    original_sheet = Sheet(original_excel, "原始")
    print(original_sheet.get_row_number())

