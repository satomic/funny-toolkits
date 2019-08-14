# coding=utf-8

from datetime import datetime
import openpyxl # 需要升级到最新的2.6.2版本 python -m pip install --upgrade openpyxl
from datacollector.common.common import print_info
from datacollector.excel.excel_utils import Sheet
from sys import argv
import os,sys


# 原始文件名
original_excel_name = "data_sample.xlsx"
# 原始sheet名
original_sheet_name = "原始"

# 报告模板文件名
final_sheet_tamplate_file = "tamplate.xlsx"


version = '20190707v1'

# main方法调用则传入真实参数
work_dir = os.path.dirname(argv[0])


def notice():
    print( \
        '''
        exe后面需要带入以下参数
        original_sheet_name 原始(默认值)
        -v version
        -h help
        ''')

if len(argv) == 1:
    if not argv[0].endswith(".py"):
        notice()
        sys.exit(0)

if len(argv) == 2:
    argv_1 = argv[1]
    if argv_1 in ["-v","-V","-version","--version"]:
        print("version: %s" % version)
        sys.exit(0)
    if argv_1 in ["-h","-H","-help","--help"]:
        notice()
        sys.exit(0)
    original_excel_name = argv[1]

if len(argv) == 3:
    original_excel_name = argv[1]
    original_sheet_name = argv[2]

# 载入原始数据
original_sheet = Sheet(original_excel_name, original_sheet_name)
gongxian_danliang = original_sheet.col_values(1) # 读取第1列数据
print_info("load orignal data: %s" % gongxian_danliang)

# 载入模板文件
updater =openpyxl.load_workbook(final_sheet_tamplate_file)
sheet = updater.get_sheet_by_name('结果')
row_counter = 2
for value in gongxian_danliang[1:]: # 排除掉第一个title
    sheet.cell(row=row_counter, column=2, value=value) # 自然计数，从1开始算
    row_counter += 1
print_info("data updaed successfully")

# 保存
report_name = "result_%s.xlsx" % datetime.now().strftime('%Y%m%d_%H%M%S')
updater.save(report_name)
print_info("report generated: %s" % report_name)



