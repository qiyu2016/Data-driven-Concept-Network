# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 13:38:18 2014

@author: Shaobo
The best of all
"""

import numpy as np
import matplotlib.pyplot as plt
import random
import math

MAX = 1000000

def nearestNeighbor(index):
    dd = MAX
    neighbor = -1
    for i in range(length):
        if dist[index, i] < dd and rho[index] < rho[i]:
            dd = dist[index, i]
            neighbor = i
    if result[neighbor] == -1:
        result[neighbor] = nearestNeighbor(neighbor)
    return result[neighbor]

#Read data
fileName = input("Enter the file's name: ")
#fileName = raw_input("Enter the file's name: ")
#python3.0版本后用input替换了raw_input
location = []
label = []

#for line in open('./01transmission.txt', 'r'):
for line in open(fileName, 'r'):
    items = line.strip().split(' ')
#    label.append(int(items.pop()))
    tmp = []
    for item in items:
        tmp.append(float(item))
    location.append(tmp)
location = np.array(location)
#label = np.array(label)
length = len(location)

#pop()函数用于移除列表中的一个元素(默认最后一个元素)，并且返回该元素的值

#Caculate distance
dist = np.zeros((length, length))   #返回一个指定形状的数组，此为行和列均为length的数组
ll = []
begin = 0
while begin < length-1:
    end = begin + 1
    while end < length:
        dd = np.linalg.norm(location[begin]-location[end])   #np.linalg.norm求范数，默认二范数，在此即为两点之间的距离
        dist[begin][end] = dd
        dist[end][begin] = dd
        ll.append(dd)
        end = end + 1
    begin = begin + 1
ll = np.array(ll)
# Algorithm        
#percent = float(raw_input("Enter the average percentage of neighbours: "))
percent = 2.0
position = int(len(ll) * percent / 100)
sortedll = np.sort(ll)  #排序函数(直接将ll改变) 此为升序一维
dc = sortedll[position] #阈值   此为取数据点间的距离总数据量的2%的点间距为阈值

file = open('./cluster_center_py.txt', 'a', encoding='utf8')
file.write(fileName + '\n')
file.write('Computing Rho with gaussian kernel of radius:   ' + str(dc) + '\n')


#求点的局部密度(local density)
rho = np.zeros((length, 1))
begin = 0   #这两个循环巧妙，值得学习
while begin < length-1:
    end = begin + 1
    while end < length:
        rho[begin] = rho[begin] + math.exp(-(dist[begin][end]/dc) ** 2)   #exp(-x**2)需要了解下
        rho[end] = rho[end] + math.exp(-(dist[begin][end]/dc) ** 2)
        #if dist[begin][end] < dc:
        #    rho[begin] = rho[begin] + 1
        #    rho[end] = rho[end] + 1
        end = end + 1
    begin = begin + 1

#求比点的局部密度大的点到该点的最小距离
delta = np.ones((length, 1)) * MAX   #np.ones()函数可以创建任意维度和元素个数的数组，其元素值均为1
maxDensity = np.max(rho)
begin = 0
while begin < length:
    if rho[begin] < maxDensity:
        end = 0
        while end < length:
            if rho[end] > rho[begin] and dist[begin][end] < delta[begin]:
                delta[begin] = dist[begin][end]
            end = end + 1
    else:
        delta[begin] = 0.0
        end = 0
        while end < length:
            if dist[begin][end] > delta[begin]:
                delta[begin] = dist[begin][end]
            end = end + 1
    begin = begin + 1

#rate1 = 0.6
#Aggregation Spiral 0.6
#Jain Flame 0.8
#D31 0.75
#R15 0.6
#Compound 0.5
#Pathbased 0.2
#thRho = rate1 * (np.max(rho) - np.min(rho)) + np.min(rho)

#rate2 = 0.2
#Aggregation Spiral 0.2
#Jain Flame 0.2
#D31 0.05
#R15 0.1
#Compound 0.08
#Pathbased 0.4
#thDel = rate2 * (np.max(delta) - np.min(delta)) + np.min(delta)



#确定聚类中心
#result = np.ones(length, dtype=np.int) * (-1)
#center = 0
#items = range(length)
#random.shuffle(items)
#for i in range(length): #items:
#    if rho[i] > thRho and delta[i] > thDel:
#        result[i] = center
#        center = center + 1


#赋予每个点聚类类标
#for i in range(length):
#    dist[i][i] = MAX

#for i in range(length):
#    if result[i] == -1:
#        result[i] = nearestNeighbor(i)
#    else:
#        continue

plt.plot(rho, delta, '.')
plt.xlabel('rho'), plt.ylabel('delta')
plt.show()


#计算gamma值
gamma = np.zeros((length, 1))   #定义gamma
for i in range(length):
    gamma[i] = rho[i]*delta[i]
gamma_sorted = sorted(gamma, reverse = True)   #list的sort方法返回的是对已经存在的列表进行操作，而内建函数sorted方法返回的是一个新的list,而不是在原来的基础上进行的操作；   sorted()可以利用参数reverse = True进行反向排序


#聚类个数q, because(gamma_sorted[]从0开始编号)
q = 3

#初始化cluster个数
center = 0

#确定聚类中心
result = np.ones(length, dtype=np.int) * (-1)
icl = []
#icl = np.zeros((length, 1))
for i in range(length): #items:
    if gamma[i] > gamma_sorted[q]:
        center = center + 1
        result[i] = center     #第i号数据点是第center类的聚类中心
        icl.append(i)   #逆映射，第center个cluster的中心为第i号数据点

file.write('Number of Clusters:   ' + str(center) + '\n')
for i in range(center):
    file.write('Cluster_' + str(i+1) +': ' + str(icl[i]+1) + '   location:' + str(location[icl[i]]) + '\n')

file.write('\n')
file.close()


#赋予每个点聚类类标
for i in range(length):
    dist[i][i] = MAX

for i in range(length):
    if result[i] == -1:
        result[i] = nearestNeighbor(i)
    else:
        continue



#range(),创建整数列表(导致“TypeError: ‘range’ object does not support item assignment”),however, range()返回的是“range object”，而不是实际的list值。solving: 将range()改为list(range())
R = list(range(256))
random.shuffle(R)
R = np.array(R)/255.0
G = list(range(256))
random.shuffle(G)
G = np.array(G)/255.0
B = list(range(256))
random.shuffle(B)
B = np.array(B)/255.0
colors = []
for i in range(256):
    colors.append((R[i], G[i], B[i]))

plt.figure()
for i in range(length):
    index = result[i]
    plt.plot(location[i][0], location[i][1], color = colors[index], marker = '.')
plt.xlabel('x'), plt.ylabel('y')
plt.show()
#
#plt.figure()
#for i in range(length):
#    index = label[i]
#    plt.plot(location[i][0], location[i][1], color = colors[index], marker = '.')
#plt.xlabel('x'), plt.ylabel('y')
#plt.show()
