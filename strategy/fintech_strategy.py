# -*- coding:utf-8 -*-
# Fintech-Homework
# Python

import json
import random
from datetime import datetime

import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

def calculate_monthly_sharp_ratio(df, month_range, asset):
    monthly_dict = {
        'Asset' : asset,
        'Month' : [],
        'Standard_Variance' : [],
        'Return_Ratio' : [],
        'Sharp_Ratio' : [],
    }
    for i in range(0, len(month_range) - 1):
        month =  datetime.strptime(df["Date"][month_range[i]], '%d/%m/%Y').date().month
        monthly_dict['Month'].append(month)
        monthly_std = df[asset][month_range[i]:month_range[i + 1]].std()
        monthly_dict['Standard_Variance'].append(monthly_std)
        monthly_return = 1
        for daily_return in df[asset][month_range[i]:month_range[i + 1]]:
            monthly_return = monthly_return * (1 + daily_return)
        monthly_return = monthly_return - 1
        monthly_dict['Return_Ratio'].append(monthly_return)
        if monthly_return >= 0:
            monthly_sharp_ratio = monthly_std / monthly_return
        else:
            monthly_sharp_ratio = 0
        monthly_dict['Sharp_Ratio'].append(monthly_sharp_ratio)
    return monthly_dict

def fintech_strategy(df, asset_dict):
    cash = 10000000000
    cash_list = []
    revenue_list = []
    print len(asset_dict['Asset1']['Month'])
    for i in range(0, len(asset_dict['Asset1']['Month'])):
        #如果是奇数月，则此类数据作为选股依据，根据Sharp_Ratio选取最高的十只股票，返回Asset—Name-List，并依据该List将下个月数据加入回测
        if ((asset_dict['Asset1']['Month'][i]) % 2) != 0:
            selected_dict = {

            }
            for asset_name in df.columns[1:]:
                if asset_dict[asset_name]['Sharp_Ratio'][i] >0:
                    selected_dict[asset_name] = asset_dict[asset_name]['Sharp_Ratio'][i]

            #在这里对所有该月所有股票进行选股，将名单交给下个月
            stock_list = sorted(selected_dict.items(), key=lambda d: d[1], reverse=True)
            stock_list = stock_list[5:15]
            print "该月份选股："
            print stock_list

            #回测
            revenue = 0
            revenue = backtest(cash=cash, j=i+1, stock_list=stock_list, asset_dict=asset_dict)
            cash = revenue + cash
            cash_list.append(cash)
            revenue_list.append(revenue)
    print "============="
    print "============="
    print "============="
    print "历史回测最终收益："
    print cash
    return cash_list

#Backtest
def backtest(cash, j, stock_list, asset_dict):
    single_stock_revenue = cash / 10
    revenue = 0
    print "该月份依据上月选股收益率："
    for item in stock_list:
        revenue = revenue + (asset_dict[item[0]]['Return_Ratio'][j]) * single_stock_revenue
        print asset_dict[item[0]]['Return_Ratio'][j]
        print '-------------------'
    print "该回测月份收益为："
    print revenue
    print '+++++++++++++++'
    return revenue


if __name__ == '__main__':
    df = pd.read_csv("data/assets.csv")
    asset_list = df.columns
    data_list = [datetime.strptime(d, '%d/%m/%Y').date() for d in df['Date']]
    month_range = [0]
    asset_dict = {

    }
    for i in range(0,7359):
        if data_list[i].month != data_list[i+1].month:
            month_range.append(i+1)
    for asset_name in asset_list[1:]:
        asset_monthly_dict={}
        asset_monthly_dict = calculate_monthly_sharp_ratio(df=df, month_range=month_range, asset = asset_name)
        asset_dict[asset_name] = asset_monthly_dict
    revenue_list = fintech_strategy(df=df, asset_dict=asset_dict)
    print revenue_list
    plt.title('Sharp-Ratio月度回测收益曲线',fontsize='large',fontweight='bold')
    plt.plot(revenue_list)
    plt.ylabel('Revenue')
    plt.xlabel('Year')
    plt.show()
