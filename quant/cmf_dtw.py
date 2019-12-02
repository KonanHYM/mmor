# -*- coding: utf-8 -*-
# Cmf DTW strategy
# Python

from dtw import dtw

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.spatial.distance import euclidean

#Example
# x = np.array([[1,1], [2,2], [3,3], [4,4], [5,5]])
# y = np.array([[2,2], [3,3], [4,4]])
# print fastdtw(x, y, dist=euclidean)
# exit()
# distance, path = fastdtw(x, y, dist=euclidean)
# print(distance)
# print(path)
# exit()

import threading
import time
from datetime import datetime


# np.std:计算矩阵的标准差（方差的算术平方根）
def normalization(x):
    return (x - np.mean(x)) / np.std(x)

# 计算皮尔逊相关系数，用于度量两个变量之间的相关性，其值介于-1到1之间
def corrcoef(a,b):
    corrc = np.corrcoef(a,b)
    corrc = corrc[0,1]
    return (16 * ((1 - corrc) / (1 + corrc)) ** 1) # ** 表示乘方

# 定义自定义线程类
class Thread_Local(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter
        self.__running = threading.Event() # 标识停止线程
        self.__running.set() # 设置为True

    def run(self):
        print("starting %s" % self.name)
        self.split_data(self.counter) # 执行代码逻辑

    def stop(self):
        self.__running.clear()

    # 分割片段并执行匹配，多线程
    def split_data(self, split_len):
        base = data_points[basebegin:basebegin+baselen]  # 获取初始要匹配的数据
        subseries = []
        dateseries = []
        for j in range(0, length):
            if (j < (basebegin - split_len) or j > (basebegin + split_len - 1)) and j <length - split_len:
                subseries.append(data_points[j:j+split_len])
                dateseries.append(j) #开始位置
        self.search(subseries, base, dateseries)  # 调用模式匹配

    def search(self, subseries, base, dateseries):
    # 片段搜索
        listdistance = []
        for i in range(0, len(subseries)):
            tt = np.array(subseries[i])
            dist, cost, acc, path = dtw(base, tt, dist=euclidean)
            listdistance.append(dist)
            # distance = corrcoef(base, tt)
            # listdistance.append(distance)
        # 排序
        index = np.argsort(listdistance, kind='quicksort') #排序，返回排序后的索引序列
        result.append(subseries[index[0]])
        print("result length is %d" % len(result))
        base_list.append(base)
        date_list.append(dateseries[index[0]])
        # 关闭线程
        self.stop()

if __name__ == '__main__':

    print("begin Main Thread")
    startTimeStamp = datetime.now() # 获取当前时间
    # 加载数据
    filename = 'price_data/BTCUSD.csv'
    # 获取第一，二列的数据
    all_date = pd.read_csv(filename, dtype = 'str')
    all_date = np.array(all_date)
    quit
    data = all_date[:, 2]
    times = all_date[:, 1]

    data_points = pd.read_csv(filename, usecols = ["open_price"])
    data_points = np.array(data_points)
    data_points = data_points[:,0] #数据

    topk = 10 #只显示top-10
    baselen = 100 # 假设在50到150之间变化
    basebegin = 0
    basedata = data[basebegin]+' '+times[basebegin]+'~'+data[basebegin+baselen-1]+' '+times[basebegin+baselen-1]
    length = len(data_points) #数据长度

    # 定义结果变量
    result = []
    base_list = []
    date_list = []

    print range(int(round(0.5 * baselen)), int(round(1.5 * baselen)), 10)
    # 变换数据（收缩或扩展），生成50到150之间的数据，间隔为10
    loc = 0
    for split_len in range(int(round(0.5 * baselen)), int(round(1.5 * baselen)), 10):
        # 执行匹配
        thread = Thread_Local(1, "Thread" + str(loc), split_len)
        loc += 1
        # 开启线程
        thread.start()

    boo = 1

    while(boo > 0):
        if(len(result) < 10):
            if(boo % 100 == 0):
                print("has running %d s" % boo)
                boo += 1
                time.sleep(1)
            else:
                boo = 0

    # 片段搜索
    listdistance = []
    for i in range(0, len(result)):
        tt = np.array(result[i])
        dist, cost, acc, path = fastdtw(base_list[i], tt, dist=euclidean)
        # distance = corrcoef(base_list[i], tt)
        listdistance.append(dist)
        # 最终排序
        index = np.argsort(listdistance, kind='quicksort') #排序，返回排序后的索引序列
        print("closed Main Thread")
        endTimeStamp = datetime.now()
        # 结果集对比
        plt.figure(0)
        plt.plot(normalization(base_list[index[0]]),label= basedata,linewidth='2')
        length = len(result[index[0]])
        begin = data[date_list[index[0]]] + ' ' + times[date_list[index[0]]]
        end = data[date_list[index[0]] + length - 1] + ' ' + times[date_list[index[0]] + length - 1]
        label = begin + '~' + end
        plt.plot(normalization(result[index[0]]), label=label, linewidth='2')
        plt.legend(loc='lower right')
        plt.title('normal similarity search')
        plt.show()
        print('run time', (endTimeStamp-startTimeStamp).seconds, "s")
