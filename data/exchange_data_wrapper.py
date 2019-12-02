# -*- coding:utf-8 -*-
# 获取数字货币历史数据
# Python

import ccxt

import json
import time
import pandas as pd

from permissions import binance

class DataWrapper(object):
    """docstring for ."""
    def __init__(self, exchange):
        self.exchange = exchange

    #根据ticker获取历史数据，并保存到文件夹中的CSV文件中
    def get_history_data(self, ticker):
        return self.exchange.fetchOHLCV(ticker, '1d')

        # name_list = ['time','open_price','high_price','low_price','close_price','volume','return']
        # data_list = []
        # for item in self.exchange.fetchOHLCV(ticker, '1d'):
        #     ltime=time.localtime(int(str(item[0])[:-3]))
        #     timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
        #     return_rate = (item[4] - item[1]) / item[1]
        #     mete_data_list = [timeStr, item[1],item[2],item[3],item[4],item[5],return_rate]
        #     data_list.append(mete_data_list)
        # csv_pd = pd.DataFrame(columns=name_list, data=data_list)
        # file_path = ticker.split('/')[0] + ticker.split('/')[1] + ".csv"
        # csv_pd.to_csv(file_path, encoding='gbk')

    def get_ticker_info(self, ticker, params = None):
        return self.exchange.fetchTicker(ticker, params)

    #获取账户余额
    def get_balance(self):
        balance = self.exchange.fetchBalance()
        return balance

if __name__ == '__main__':
    #获取交易所对象
    exchange_id = 'binance'
    exchange_class = getattr(ccxt, exchange_id)

    #对交易所秘钥进行设置
    exchange = exchange_class(binance)
    binance_data_parser = DataWrapper(exchange = exchange)

    #获取该交易所所有交易对，声称ticker_list
    ticker_list = []
    for item in exchange.fetchMarkets():
        single_ticker = item['symbol']
        ticker_list.append(single_ticker)
    print ticker_list

    #获取交易所中所存货币余额
    print binance_data_parser.get_ticker_info(ticker = 'BTC/USDT')
