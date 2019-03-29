#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header :
    
This program illustrates a new match algorithm which combines the note_extraction from Silvet 
pitch active results and match correction with a LCS and Cosine algorithms.

@author: alex-geng, brother-nan
"""


import LCS as LCS
import csv
import numpy as np
import time
import json
import boundary_check as BC


#记录程序开始时间：
time_start = time.clock()


#将sp和tp的时间序列存储为list -- SP_TIME,TP_TIME:
SP_TIME=[]
with open('sp_cut_note_pitch_active.csv','r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        SP_TIME.append(row['time_point'])  
TP_TIME=[]
with open('tp_cut_note_pitch_active.csv','r') as g:
    reader = csv.DictReader(g)
    for row in reader:
        TP_TIME.append(row['time_point'])  

#读取sp_beat信息并保存为list--CUT:        
CUT = []
with open('sp_cut_beat.csv','r') as h:
    for row in h.readlines():
        CUT.append(row.strip('\n'))


#按照beat信息对sp进行切分
MAX_SEG = []

#sp_start&end从列表CUT中选取，即按照beat时间点来选取
sp_start = CUT[0]
sp_end = CUT[3]
index = 3

#len_tp为一个相对于TP总长度的常量（此处设定为总长的1/100），在下面的迭代过程中我们设定迭代上限为len_tp*3以节约运行时间
len_tp = len(TP_TIME)//100
tp_start = 0
#设定tp_end的迭代步长为--2：
tp_end = tp_start + 2


while index+1 < len(CUT) and tp_end <len(TP_TIME):
    #初始化匹配值identity为空：
    IDENTITY = []

    #二分法查找由beat得出的sp_start&sp_end的时间对应在SP_TIME中的时间：
    T1 = SP_TIME[ BC.binary_search(SP_TIME,float(sp_start)) ]
    T2 = SP_TIME[ BC.binary_search(SP_TIME,float(sp_end)) ]
    
    T3 = TP_TIME[tp_start]
    while tp_end <= tp_start+len_tp*3 and tp_end < len(TP_TIME):
        #以步长 2开始迭代运算tp_start+2到tp_start+len_tp*3的所有tp_start&tp_end区间对应的 Identity：
        #保存时，将identity值保存为IDENTITY第一列，将对应的tp_end值保存为IDENTITY第二列，方便之后读取tp_end:
        IDENTITY.append([LCS.lcs(T1,T2,T3,TP_TIME[tp_end]),tp_end])   
        tp_end += 2
    
    #防止出现空集报错
    if IDENTITY != []:
        #将IDENTITY转化为numpy矩阵：
        IDENTITY = np.array(IDENTITY)
        #取identity第一列中的最大值对应的index:
        MAX_ID = np.argmax(IDENTITY,axis=0)
        #将sp_start,sp_end，tp_start，identity最大值对应的tp_end保存到MAX_SEG中：
        if (int(IDENTITY[MAX_ID[0]][1])+10)<len(TP_TIME):
            MAX_SEG.append([sp_start,sp_end,TP_TIME[tp_start],TP_TIME[int(IDENTITY[MAX_ID[0]][1])+10]])
        else:
            MAX_SEG.append([sp_start,sp_end,TP_TIME[tp_start],TP_TIME[int(IDENTITY[MAX_ID[0]][1])]])
    #设定下一次循环的sp_start&end, tp_start&end值：    
    tp_end = int(IDENTITY[MAX_ID[0]][1])
    #index+1， 移动至下一个beat
    sp_start = CUT[index]
    sp_end = CUT[index+4]
    index += 4
    #以上一个tp_end为新的tp_start，新的tp_end为新的tp_start+2
    tp_start = tp_end
    tp_end = tp_start+2
    
print(MAX_SEG)
#保存结果为temp_match.csv:
with open("temp_match_7.csv","w") as csvfile:
    for row in MAX_SEG:
        csvfile.write(json.dumps(row)+"\n")


"""
#初始化切分间隔：
len_sp = len(SP_TIME)//100
len_tp = len(TP_TIME)//100

#切分:
sp_start = 0
sp_end = 0
tp_start = 0
tp_end = 0
MAX_SEG = []
sp_start = sp_end
sp_end = sp_start + len_sp
tp_start = tp_end
tp_end = tp_start+len_tp//10

#切分sp的最小间隔为10
while sp_end < len(SP_TIME) and tp_end <len(TP_TIME):

    IDENTITY = []

    T1 = SP_TIME[sp_start]
    T2 = SP_TIME[sp_end]
    T3 = TP_TIME[tp_start]
    while tp_end <= tp_start+len_tp*3 and tp_end <len(TP_TIME):

        IDENTITY.append([LCS.lcs(T1,T2,T3,TP_TIME[tp_end]),tp_end])   
        tp_end += len_tp//10
    if IDENTITY != []:
        
        IDENTITY = np.array(IDENTITY)
        MAX_ID = np.argmax(IDENTITY,axis=0)
        MAX_SEG.append([SP_TIME[sp_start],SP_TIME[sp_end],TP_TIME[tp_start],TP_TIME[int(IDENTITY[MAX_ID[0]][1])]])
        tp_end = int(IDENTITY[MAX_ID[0]][1])
    sp_start = sp_end
    sp_end = sp_start + len_sp
    tp_start = tp_end
    tp_end = tp_start+len_tp//10
    
print(MAX_SEG)

with open("temp_match_2.csv","w") as csvfile:
    for row in MAX_SEG:
        csvfile.write(json.dumps(row)+"\n")

#sp_start = MAX_SEG[0,0]
#sp_end = MAX_SEG[0,1]
#tp_start = MAX_SEG[0,2]
#tp_end = MAX_SEG[0,3]
#len_sp = len_sp//5
#len_tp = len_tp//5

"""



print(MAX_SEG)
#打印程序运行时间：       
time_elapsed = time.clock()-time_start
print("Time consumed in this Program: ",time_elapsed,'\n')        
        
        



