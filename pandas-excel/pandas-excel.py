# coding=utf-8

import pandas as pd

import argparse
import traceback
import time
import datetime

# parser.add_argument('host', type=str, help="socket server IP") must be set
# parser.add_argument('--host', type=str, help="socket server IP") can be free


# def read_excel(io, sheetname=0, header=0, skiprows=None, skip_footer=0,
#                index_col=None, parse_cols=None, parse_dates=False,
#                date_parser=None, na_values=None, thousands=None,
#                convert_float=True, has_index_names=None, converters=None,
#                engine=None, **kwds):

excel_file = r"persons.xlsx"
df_persion = pd.read_excel(open(excel_file,'rb'), sheetname="Sheet1")
print df_persion