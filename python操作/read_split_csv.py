import csv
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split

"""
python将大csv文件划分成小csv文件做训练集和测试集及对应label文件
"""

def read_data(test_data='input/train.csv', n=0, label=1):
    '''
    加载数据的功能
    n:特征数据起始位
    label：是否是监督样本数据
    '''
    csv_reader = csv.reader(open(test_data, encoding="utf8", errors="ignore"))
    data_list = []
    for one_line in csv_reader:
        data_list.append(one_line)
    x_list = []
    y_list = []
    for one_line in data_list[1:]:
        if label == 1:#如果是监督样本数据
            y_list.append(int(one_line[-1]))  # 标志位(最后一位都是标签位)
            one_list = [o for o in one_line[n:-1]]
            x_list.append(one_list)
        else:
            one_list = [o for o in one_line[n:]]
            x_list.append(one_list)
    return x_list, y_list

def split_data(data_list, y_list, ratio=0.30):#70%训练集，30%测试集: 914285,391837
    '''
    按照指定的比例，划分样本数据集
    ratio: 测试数据的比率
    '''
    X_train, X_test, y_train, y_test = train_test_split(data_list, y_list, test_size=ratio, random_state=50)

    """训练集"""
    with open('input/sub_train.csv', 'w', encoding="utf8",newline="", errors="ignore") as csvfile:#不加newline=""的话会空一行出来
        fieldnames = ['qid', 'question_text','target']
        write = csv.DictWriter(csvfile,fieldnames=fieldnames)
        write.writeheader()#写表头
        for i in range(len(X_train)):
           write.writerow({'qid':X_train[i][0],'question_text':X_train[i][1],'target':y_train[i]})

    """测试集"""
    #标签文件
    with open('input/sub_test_y', 'w') as fp:
        json.dump(y_test, fp)
    #测试csv
    with open('input/sub_test_x.csv', 'w', encoding="utf8",newline="", errors="ignore") as csvfile:#不加newline=""的话会空一行出来
        fieldnames = ['qid', 'question_text']
        write = csv.DictWriter(csvfile,fieldnames=fieldnames)
        write.writeheader()#写表头
        for i in range(len(X_test)):
           write.writerow({'qid':X_test[i][0],'question_text':X_test[i][1]})
    return X_train, X_test, y_train, y_test

if __name__ == '__main__':
    """获取大文件的数据"""
    x_list, y_list=read_data()
    """划分为训练集和测试集及label文件"""
    split_data(x_list,y_list)
