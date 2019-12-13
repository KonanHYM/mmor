# -*- coding:utf-8 -*-
# PET Parser

import numpy as np
import pandas as pd

import math
import json


#设置文件路径
PET_FILE = "pet_files/502072596"

#
#电子银行承兑汇票的文件结构
PET_DATA = {
    "acpdat" : '',#出票日期
    "acpstat" : '',#票据状态
    "acparrdat" : '',#汇票到期日
    "acpcode" : ''，#票据号码

    #出票人信息
    "acpinfo" : {
        "acpnam" : '', #出票人全称
        "acpaccount" : '',  #出票人账号
        "acpbam" : ''  #开户银行
    },
    #收款人信息
    "rcvinfo" : {
        "rcvnam" : "",  #收款人全称
        "rcvaccount" : '',    #递延税
        "rcvbam" : ''
    },

    "Equity" : {
        "CurrentNI" : 10791000.00,
        "ShareholderEquity" : 108089000.00,
        "TotalEquity" : 118880000.00,
    },
    "Revenue" : {
        "Revenue" : 221600000.00,

    },
    "Expense" : {
        "COGS" : 161100000.00,
        "ManufacturingCosts" : 16000000.00,
        "SG&A" : 13600000.00,
        "D&A" : 8700000.00,
        "Gain&Loss" : 0.00,
    },
    "NI": {
        "WorkingCapital" : 37121000.00,
        "GrossProfit" : 60600000.00,
        "OperatingIncome":31000000.00,
        "EBIT" : 31000000.00,
        "EBITDA" : 39700000.00,
        "NI" : 10791000,
    }
}

Ratios_Data = {
    "ActivityRatios" : {
        "receivables turnover" : "CANNOT CALCULATE",
        "days of sales outstanding" : "CANNOT CALCULATE",
        "payables turnover" : "CANNOT CALCULATE",
        "days payables outstanding" : "CANNOT CALCULATE",
        "inventory turnover" : "CANNOT CALCULATE",
        "days inventory outstanding" : "CANNOT CALCULATE",
        "total asset turnover" : "CANNOT CALCULATE",
        "fixed asset turnover" : "CANNOT CALCULATE",
        "working capital turnover" : "CANNOT CALCULATE",
    },
    "LiquidityRatios" : {
        "current ratio" : "CANNOT CALCULATE",
        "quick ratio" : "CANNOT CALCULATE",
        "cash ratio" : "CANNOT CALCULATE",
        "defensive interval" : "CANNOT CALCULATE",
        "cash conversion cycle" : "CANNOT CALCULATE",
    },
    "SolvencyRatios" : {
        "debt to equity" : "CANNOT CALCULATE",
        "debt to assets" : "CANNOT CALCULATE",
        "financial_leverage" : "CANNOT CALCULATE",
        "interset coverage" : "CANNOT CALCULATE",
        "fixed charge coverage" : "CANNOT CALCULATE",
    },
    "ProfitabilityRatios" : {
        "net_profit_margin" : "CANNOT CALCULATE",
        "gross_profit_margin" : "CANNOT CALCULATE",
        "operating_profit_margin" : "CANNOT CALCULATE",
        "pretax margin" : "CANNOT CALCULATE",
        "ROA" : "CANNOT CALCULATE",
        "ROE" : "CANNOT CALCULATE",
    },

}

def Pet_Parser():
    final = pd.read_excel(PET_FILE)

    for final_types in final.columns:
        print final_types

if __name__ == '__main__':
    Pet_Parser()
