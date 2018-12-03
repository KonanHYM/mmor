# -*- coding:utf-8 -*-
# 获取数字货币历史数据
# Python

import ccxt
import json
import time
import pandas as pd

class ccxtParser(object):
    """docstring for ."""
    def __init__(self, exchange):
        self.exchange = exchange

    #根据ticker获取历史数据，并保存到文件夹中的CSV文件中
    def getHistoryData(self, ticker):
        name_list = ['time','open_price','high_price','low_price','close_price','volume','return']
        data_list = []
        for item in exchange.fetchOHLCV(ticker, '1d'):
            ltime=time.localtime(int(str(item[0])[:-3]))
            timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
            return_rate = (item[4] - item[1]) / item[1]
            mete_data_list = [timeStr, item[1],item[2],item[3],item[4],item[5],return_rate]
            data_list.append(mete_data_list)
        csv_pd = pd.DataFrame(columns=name_list, data=data_list)
        file_path = ticker.split('/')[0] + ticker.split('/')[1] + ".csv"
        csv_pd.to_csv(file_path, encoding='gbk')
        print file_path

if __name__ == '__main__':
    #获取交易所对象
    exchange_id = 'bittrex'
    exchange_class = getattr(ccxt, exchange_id)
    #对交易所秘钥进行设置
    exchange = exchange_class({
        'apiKey': 'YOUR_API_KEY',
        'secret': 'YOUR_SECRET',
        'timeout': 30000,
        'enableRateLimit': True,
        })
    ccxt_parser = ccxtParser(exchange=exchange)
    #获取该交易所所有交易对，声称ticker_list
    ticker_list = []
    for item in exchange.fetchMarkets():
        single_ticker = item['symbol']
        print single_ticker
        ticker_list.append(single_ticker)
    print len(ticker_list)

    ccxt_parser.getHistoryData(ticker='BTC/USDT')

    #获取每个ticker的历史数据，并保存到CSV中
    # for single_ticker in ticker_list:
    #     if single_ticker in complete_list:
    #         continue
    #     ccxt_parser.getHistoryData(ticker=single_ticker)
    #     time.sleep(5)
