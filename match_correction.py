#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header:

This program is used to calculate the note-matching compatibility between two slices of audio :
Function: match_comparasion(sp_start,sp_end,tp_start,tp_end)
输入sp和tp中对应的起始时间节点，输出匹配度矩阵compatibility: Comp

@author: alex
"""

import pandas as pd
import csv
import json

def match_comparasion(sp_start,sp_end,tp_start,tp_end):
    #打开相应的tp单音信息文件pitch_active.csv并依据 start & end 时间值截取响应片段，另做保存为字典文件list_tp & list_sp：
    with open('sp_pitch_active.csv','r') as f:
        reader = csv.DictReader(f)
        list_sp = [json.loads(row['pitch_names']) for row in reader if float(row['time_point']) >= sp_start and float(row['time_point']) <= sp_end]  

    with open('tp_pitch_active.csv','r') as h:
        reader = csv.DictReader(h)
        list_tp = [json.loads(row['pitch_names']) for row in reader if float(row['time_point']) >= tp_start and float(row['time_point']) <= tp_end]  
    #注意，该字典的键值是str，相对应的元素是由str组成的list
    #将时间片段转换成1维list：note_sp,note_tp
    note_sp = []
    for i in range(len(list_sp)):
        note_sp += list_sp[i]
    
    note_tp = []
    for i in range(len(list_tp)):
        note_tp += list_tp[i]
    #统计该时间片段里出现的单音值（去重后）与其相应的重复次数：
    note_sp=pd.value_counts(note_sp)
    note_sp= sorted(note_sp.items(), key=lambda x: x[0], reverse=False)
    note_tp=pd.value_counts(note_tp)
    note_tp= sorted(note_tp.items(), key=lambda x: x[0], reverse=False)
    
    #获取onset处的单音信息：

    if len(list_sp) != 0:
        onset_sp=list_sp[0]
    else:
        onset_sp=[]
        
    if len(list_tp) != 0:
        onset_tp=list_tp[0]
    else:
        onset_tp=[]
        
    #获取offset处的单音信息：
    if len(list_sp) != 0:
        offset_sp=list_sp[-1]
    else:
        offset_sp=[]
    
    if len(list_tp) != 0:
        offset_tp=list_tp[-1]
    else:
        offset_tp=[]
    
    #开始计算匹配度，并生成匹配度矩阵 : Comp
    Comp = [0,0,0]
    # section 1: 计算单音匹配度 Comp[0], 以及相应单音在note_sp,note_tp中的index
    Comp0 = 0
    index_sp = []
    index_tp = []
    temp = [row[0] for row in note_tp]
    for i in range(len(note_sp)):
        if note_sp[i][0] in temp:
            Comp0 += 1
            index_sp.append(i)
            index_tp.append(temp.index(note_sp[i][0]))
    #分母加1是为了防止分母为零
    Comp[0] = Comp0/(len(note_sp)+len(note_tp)+1)
   
    # section 2: 计算单音duration匹配度
    Comp1 = 0
    j= 0
    for i in index_sp:
        Comp1 += 1-abs(note_sp[i][1]-note_tp[index_tp[j]][1])/(note_sp[i][1]+note_tp[index_tp[j]][1])
        j += 1
    
    #分母加1是为了防止分母为零
    Comp[1] = Comp1/(len(index_sp) + 1)
        
    # section 3: 计算boundary匹配度
    Comp2 = 0
    for k in onset_sp:
        if k in onset_tp:
            Comp2 += 1
    for g in offset_sp:
        if g in offset_tp:
            Comp2 += 1
    
    #分母加1是为了防止分母为零
    Comp[2] = Comp2/(len(onset_sp)+len(offset_sp)+1)    
    
    return Comp

#该函数定义了比较Comp大小的方法，match、beat的结果分别作为Comp1、Comp2输入：
def max_comparasion(Comp1,Comp2):
    # 1--match， 2--beat
    for k in range(len(Comp1)):
        if Comp1[k] > Comp2[k]:
            #match结果更好
            return 1
        elif Comp1[k] < Comp2[k]:
            #beat结果更好
            return 2
        else:
            continue
    #两者一样，那就按照match结果来改
    return 2
            
def max_comparasion1(Comp1,Comp2):
    # 1--match， 2--beat
    for k in range(len(Comp1)):
        if Comp1[k] > Comp2[k]:
            #match结果更好
            return Comp1
        elif Comp1[k] < Comp2[k]:
            #beat结果更好
            return Comp2
        else:
            continue
    #两者一样，那就按照match结果来改
    return Comp2

#test:
#Comp_match=match_comparasion_preprocessing(3.5,4,5,6)
#cc=[1,2,3]
#dd=[1,33,3]
#if max_comparasion(cc,dd) ==2:
#    print('ll')


