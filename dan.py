import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import numpy as np

import statsmodels.api as sm
from statsmodels.formula.api import ols
import tushare as ts

df_capm = pd.read_excel('code.xlsx')
print df_capm.tail()

df_rf = pd.read_excel('risk-free.xlsx')
df_rf = df_rf.set_index(['Date'])
print df_rf.tail()

stock = DataFrame()
stock = ts.get_hist_data(code = str(df_capm.loc[12, 'stkcd']).zfill(6), start = df_capm.loc[12, 'Startday'], end = df_capm.loc[12, 'Endday'])
stock = stock[['close']]
hs300 = DataFrame()
hs300 = ts.get_hist_data(code = 'hs300', start = df_capm.loc[12, 'Startday'], end = df_capm.loc[12, 'Endday'])
hs300 = hs300[['close']]
df = pd.merge(stock, hs300, left_index = True, right_index = True, how = 'outer')
df = pd.merge(df, df_rf, left_index = True, right_index = True, how = 'outer')
df = df.dropna()
df = df.reset_index(drop = True)
print(df.loc[1, 'close_x'])
print '------------------'

for i in range(len(df)-1):
    Re1 = df.loc[i + 1, 'close_x'] / df.loc[i, 'close_x'] - 1
    Re2 = df.loc[i + 1, 'close_y'] / df.loc[i, 'close_y'] - 1
    df.loc[i + 1, 'return_x'] = Re1
    df.loc[i + 1, 'return_y'] = Re2
df['return_x_rf'] = df['return_x'] - df['risk-free']
df['return_y_rf'] = df['return_y'] - df['risk-free']
df.tail()

for i in range(len(df_capm)):
    try:
        stock = DataFrame()
        stock = ts.get_hist_data(code = str(df_capm.loc[i, 'stkcd']).zfill(6), start = df_capm.loc[i, 'Startday'], end = df_capm.loc[i, 'Endday'])
        stock = stock[['close']]
        hs300 = DataFrame()
        hs300 = ts.get_hist_data(code = 'hs300', start = df_capm.loc[i, 'Startday'], end = df_capm.loc[i, 'Endday'])
        hs300 = hs300[['close']]
        print "-------0"
    except:
        pass
    df = pd.merge(stock, hs300, left_index = True, right_index = True, how = 'outer')
    df = pd.merge(df, df_rf, left_index = True, right_index = True, how = 'outer')
    df = df.dropna()
    df = df.reset_index(drop = True)
    df['return_x'] = None
    df['return_y'] = None
    print "-------1"
    for j in range(len(df)-1):
        df.loc[j + 1, 'return_x'] = df.loc[j + 1, 'close_x'] / df.loc[j, 'close_x'] - 1
        df.loc[j + 1, 'return_y'] = df.loc[j + 1, 'close_y'] / df.loc[j, 'close_y'] - 1
        print "-------2"
    df['return_x_rf'] = df['return_x'] - df['risk-free']
    df['return_y_rf'] = df['return_y'] - df['risk-free']
    try:
        stock_hs300 = ols("return_x_rf~return_y_rf", data = df).fit()
        df_capm.loc[i, 'beta'] = stock_hs300.params[1]
        print "-------3"
    except:
        pass

print df_capm.tail()
