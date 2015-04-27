__author__ = 'Administrator'
# -*- coding:utf-8 -*-

import random as rd
import time

import os
import sys
import numpy as np
import scipy as sp

import matplotlib.pyplot as plt

from sklearn.neighbors import KNeighborsClassifier
from sklearn import  svm

#import sklearn.


def read_data():
    file_list = os.listdir('RSS')
    for j in range(len(file_list)):
        for i in range(len(file_list)):
            file_name = file_list[i]
            print type(file_name)
            if len(file_name) < 5:
                file_list.pop(i)
                break

    return file_list


# 输入wifi文件，和mac——list文件，并且处理
def file_trance(file, file_index):
    fp = open(file, 'rb')
    wifi = fp.readlines()
    fp.close()

    if (os.path.exists(r'mac_list.txt')) == True:
        fp = open('mac_list.txt', 'rb')
        mac_list = fp.readlines()
        print 'mac_list:', mac_list
        fp.close()
    fout = open(str('RSS/'+ str(file_index)), 'w')
    all_instance = np.zeros(len(mac_list) + 1)
    first = True
    print mac_list
    for line in wifi:
        if line[0] == '@':
            continue
        if line[0] == '#':
            if not first:
                for i in range(len(mac_list) + 1):
                    fout.write((str(int(all_instance[i])) + ' '))
            fout.write('\n')
            line = line.split(' ')
            line = line[1]
            line = line.split('-')
            #thetime = time.mktime([int(year), int(month), int(day), int(hours), int(line[0]), int(line[1]), 0, 0, 0])
            # print thetime
            #thetime = thetime + float(line[2]) / 1000
            # print 'thetime: ' , thetime
            #fout.write(str(thetime))
            #fout.write(' ')
            first = False
        else:
            # print 'line:', line
            line = line.split(' ')
            if str(line[0]) + '\r\n' in mac_list:
                num = mac_list.index(str(line[0]) + '\r\n')
                all_instance[num] = line[1]
            if str(line[0]) in mac_list:
                num = mac_list.index(str(line[0]))
                all_instance[num] = line[1]

def data_pre():
    point_num = len(os.listdir('RSS/')) /2.0
    all_data_in = list()
    all_data_out = list()

    for i in range(0,int(point_num-1)):
        tmp_data_in = np.loadtxt(str('RSS/'+ str(i)))
        for j in range(len(tmp_data_in[:,1])):
            all_data_in.append(tmp_data_in[j,:])
            all_data_out.append(i)
    all_data_in = np.asarray(all_data_in)
    all_data_out = np.asarray(all_data_out)
    print 'len in:',len(all_data_in), 'len_out:', len(all_data_out)


    print point_num
    return all_data_in, all_data_out

def data_witeout(data_in, data_out, per_train = 0.8):
    train_data_in = list()
    train_data_out = list()
    valid_data_in = list()
    valid_data_out = list()

    for i in range(len(data_in)):
        if rd.uniform(0,1) > 0.8:
            valid_data_in.append(data_in[i,:])
            valid_data_out.append(data_out[i])
        else:
            train_data_in.append(data_in[i,:])
            train_data_out.append(data_out[i])
    return train_data_in, train_data_out, valid_data_in, valid_data_out


if __name__ == '__main__':
    the_file_list  = read_data()
    print the_file_list
    for i in range(len(the_file_list)):
        file_trance(str('RSS/'+ the_file_list[i]),i)
    data_in, data_out = data_pre()
    print len(data_in), len(data_out)
    train_data_in, train_data_out, valid_data_in, valid_data_out = data_witeout(data_in,data_out)

    #clf = KNeighborsClassifier(n_neighbors=5)
    clf = svm.SVC()
    clf.fit(train_data_in,train_data_out)

    pre_out = clf.predict(valid_data_in)

    err_times  = 0
    for i in range(len(pre_out)):
        if int(pre_out[i] - valid_data_out[i]) != 0:
            err_times+=1

    print 'acc:', err_times /1.0/len(pre_out)
    plt.plot(pre_out-valid_data_out)
    plt.grid()
    plt.show()