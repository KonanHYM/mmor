# -*- coding:utf-8 -*-
# Fintech
# Python

import ccxt
import json
import datetime
import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv("assets.csv")
    name_list = ['Date','Open','High','Low','Close','Volume','Adj. Close']
    data_list = []
    for i in range(0,df['Date'].count()):
        d = df['Date'][i].split('/')[0]
        m = df['Date'][i].split('/')[1]
        y = df['Date'][i].split('/')[2]
        date_str = y + "-" + m + "-" + d
        price = df['Asset1'][i]
        if float(price) == 0:
            price = float(price) + 0.000000001
        meta_list = [date_str, price, price, price, price, 99999999999, price]
        data_list.append(meta_list)
    csv_pd = pd.DataFrame(columns=name_list, data=data_list)
    csv_pd.to_csv("bar_feed.csv", encoding='gbk')
