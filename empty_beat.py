#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header :
    
This program is used to detect if the current beat in sp is an empty beat，
and automatially merge all the corresponding empty beats in tp when the answer is yes.

@author: alex
"""
import csv
import json


"""
Section 1: 检测sp当前片段是否为空拍子
"""



def SP_empty_beat_detection(sp_start,sp_end):
    #读取相应时间片段的单音信息：
    with open('sp_cut_note_pitch_active.csv','r') as f:
        reader = csv.DictReader(f)
        list_sp = [json.loads(row['pitch_names']) for row in reader if float(row['time_point']) >= float(sp_start) and float(row['time_point']) <= float(sp_end)]  
    #检测该片段是否为空拍子片段,是空拍子返回True，否则返回False:
    if list_sp == []:
        return True
    else:
        return False


"""
Section 2: 检测tp当前片段是否为空拍子
"""    
def TP_empty_beat_detection(tp_start,tp_end):
    #读取相应时间片段的单音信息：
    with open('tp_cut_note_pitch_active.csv','r') as g:
        reader = csv.DictReader(g)
        list_tp = [json.loads(row['pitch_names']) for row in reader if float(row['time_point']) >= float(tp_start) and float(row['time_point']) <= float(tp_end)]  
    #检测该片段是否为空拍子片段,是空拍子返回True，否则返回False:
    if list_tp == []:
        return True
    else:
        return False


"""
Section 3: 非空拍子检测,并返回之后的第一个非空拍子的index以及空拍子的数目empty_count
"""

def SP_unempty_beat_detection(index,check,SP_BEAT):
    empty_count = 0
    while check and (index+1) < len(SP_BEAT):
        check = SP_empty_beat_detection(SP_BEAT[index],SP_BEAT[index+1])
        index += 1
        empty_count += 1
    return (index-1,empty_count-1)  
        
def TP_unempty_beat_detection(index,check,TP_BEAT):
    empty_count = 0
    while check and (index+1) < len(TP_BEAT):
        check = TP_empty_beat_detection(TP_BEAT[index],TP_BEAT[index+1])
        index += 1
        empty_count += 1
    return (index-1,empty_count-1)       
    
    
    
    
"""
Section 4: 空拍子合并修正,依据sp中的空beat信息修正tp的空beat信息，并返回tp中下一个非空拍子的index
"""    
#注意：该函数涉及对变量 TP_BEAT 的修改   
def merge_empty_beat(sp_count,tp_count,tp_index_start,tp_index_end,TP_BEAT):   
    #计算该空拍子区域的时间距离跨度distance：
    distance = float(TP_BEAT[tp_index_end])-float(TP_BEAT[tp_index_start])
    try:
        offsetting = distance/sp_count
    except ZeroDivisionError:
        return tp_index_end+1
    #当sp与tp中的空拍子数目相等时，无需处理，直接返回tp中下一个非空拍子的index:
    if sp_count == tp_count:
        return tp_index_end
    #当sp中的空拍子数目小于tp中的空拍子数目时，依据sp中的空拍子数将tp片段均分，多余beat从TP_BEAT中删除：
    elif sp_count < tp_count:
        i = 1
        while (tp_index_start+i) < tp_index_end:
            if i <= (sp_count-1):
                TP_BEAT[tp_index_start+i] = str(float(TP_BEAT[tp_index_start]) + offsetting*i)
                i += 1
            else:
                #删除多余beat，注意，删除的时候TP_BEAT中的index也会改变
                TP_BEAT.pop(tp_index_start+i)
                tp_index_end -= 1
        return tp_index_end
    #当sp中的空拍子数目大于tp中的空拍子数目时，依据sp中的空拍子数将tp片段均分，添加缺少的beat：
    else:
        #注意，当tp并没有空拍子时：
        if tp_count == 0:
            j = 1
            while j < sp_count:
                TP_BEAT.insert(tp_index_start+j,TP_BEAT[tp_index_start])
                j += 1
                tp_index_end += 1
            return tp_index_end+1
        #当tp有空拍子时：
        else:
            j = 1
            while j < sp_count:
                if (tp_index_start+j) < tp_index_end:
                    TP_BEAT[tp_index_start+j] = str(float(TP_BEAT[tp_index_start]) + offsetting*j)
                    j += 1
                else:
                    #添加缺少的beat：
                    TP_BEAT.insert(tp_index_start+j,str(float(TP_BEAT[tp_index_start]) + offsetting*j))
                    j += 1
                    tp_index_end += 1
            return tp_index_end
            
        
      
        
    
    
    

    
    
#test
    
    
    
    
    
    
    
    