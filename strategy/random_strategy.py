# -*- coding:utf-8 -*-
# Python

import json
import datetime
import random
import pandas as pd

def random_walker():
    column_list = []
    for i in range(1,60):
        ran_num =  random.randint(1,77)
        column_name = "Asset" + str(ran_num)
        column_list.append(column_name)
    return column_list

if __name__ == '__main__':
    df = pd.read_csv("data/assets.csv")
    cash = 10000000000
    #    Random Walker
    for i in range(0, df["Date"].count()):
        column_list = random_walker()
        today_revenue_list = []
        today_revenue = 0.000
        for column in column_list:
            today_revenue_list.append((cash / len(column_list)) * df[column][i])
        for revenue in today_revenue_list:
            today_revenue = today_revenue + revenue
        print "今日收益：" + str(today_revenue)
        print "日期：" + str(df['Date'][i])
        cash = cash + today_revenue
        print "总收益:" + str(cash)
        print '-------'
