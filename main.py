#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header :
    
This is the main body of our program

@author: alex
"""

import csv
import time
import empty_beat as EB
import boundary_check_1 as BC
import LCS as LCS

#记录程序开始时间：
time_start = time.clock()

"""
Section 1: Pre-Processing (Preparing the data)
"""

#Input : sp_beat, sp_note, tp_beat, tp_note, sp_match_tp.


#该函数将导入的csv文件以字典的形式读取，第一列为key，第二列往后为value：
def row_csv2dict(csv_file):
    dict_club={}
    with open(csv_file)as f:
        reader=csv.reader(f,delimiter=',')
        for row in reader:
            dict_club[row[0]]=row[1]
    return dict_club

#导入match.csv文件:
MATCH = []
with open('sp_fastdtwmatchcos_tp3.csv','r')as f:
    reader=csv.reader(f,delimiter=',')
    for row in reader:
       MATCH.append(row) 

#将MATCH的第一列提取出来保存为list-- MATCH1:
MATCH1= []
with open('sp_fastdtwmatchcos_tp3.csv','r')as ff:
    reader=csv.reader(ff,delimiter=',')
    for row in reader:
       MATCH1.append(row[0]) 

#导入sp与tp的beat文件，分别存为list--sp_beat , tp_beat:
with open('sp_cut_beat.csv','r') as g:
    SP_BEAT = []
    for line in g.readlines():
        SP_BEAT.append(line)
        
with open('tp_cut_beat.csv','r') as h:
    TP_BEAT = []
    for line in h.readlines():
        TP_BEAT.append(line)
#定义MATCH_BEAT,该二维list和修订后的TP_BEAT将是我们最后的 Output。
MATCH_BEAT = []
#note文件只在进行单音匹配度检测时，由函数内部调用，程序主体无需调用。

"""
Section 2: Drop the Beat ! Start the Loop ! 
"""

#设定当前工作索引：
#index_sp = [SP_BEAT.index(i)for i in SP_BEAT]
#index_tp = [TP_BEAT.index(j)for j in TP_BEAT]

#从index 0 开始检测
SP_INDEX = 0
TP_INDEX = 0
while (SP_INDEX+1 < len(SP_BEAT) and TP_INDEX+1 < len(TP_BEAT)):

    #判断当前index对应的beat是否为空拍子,若为空拍子则找到下一个非空拍子返回其index，并计算这之间空拍子的数目 empty_count：
    SP_empty_count = 0
    TP_empty_count = 0
    
    Check1 = EB.SP_empty_beat_detection(SP_BEAT[SP_INDEX],SP_BEAT[SP_INDEX+1]) 
    if Check1 == True:
        SP_INDEX,SP_empty_count = EB.SP_unempty_beat_detection(SP_INDEX,Check1,SP_BEAT)
        
    Check2 = EB.TP_empty_beat_detection(TP_BEAT[TP_INDEX],TP_BEAT[TP_INDEX+1])   
    if Check2 == True:
        TP_INDEX_END,TP_empty_count = EB.TP_unempty_beat_detection(TP_INDEX,Check2,TP_BEAT)   
    
    #print(SP_INDEX, TP_INDEX, Check1,Check2,SP_empty_count,TP_empty_count,TP_INDEX_END,'\n')
    #执行判断，若sp或tp中存在空拍子片段，则执行空拍子合并函数merge_empty_beat（）,然后跳过剩余语句，开始执行下一步循环
    if Check1 == True and Check2 == True:
        TP_INDEX = EB.merge_empty_beat(SP_empty_count,TP_empty_count,TP_INDEX,TP_INDEX_END,TP_BEAT)
        continue
    elif Check1 == True and Check2 == False:
        TP_INDEX = EB.merge_empty_beat(SP_empty_count,TP_empty_count,TP_INDEX,TP_INDEX,TP_BEAT)
        continue
    elif Check1 == False and Check2 == True:
        TP_INDEX = EB.merge_empty_beat(-1,TP_empty_count,TP_INDEX,TP_INDEX_END+1,TP_BEAT)-1
        SP_INDEX = SP_INDEX
        continue

    #对非空拍子进行match结果与beat结果的交叉验证，若验证成功则执行下一步循环对下一个beat单元进行检测,阈值为0.05s
    temp_index = BC.binary_search(MATCH1,float(SP_BEAT[SP_INDEX+1]))
    index = BC.binary_search( TP_BEAT, float(MATCH[temp_index][1]))
    print(SP_INDEX, TP_INDEX, index,'\n')
    
    #找到了在TP_BEAT中与SP_INDEX matching结果相对应的beat boundary：
    if index != None:
        #如果对应的index 正好就是 TP_INDEX+1
        if index == TP_INDEX+1:
            SP_INDEX += 1
            TP_INDEX += 1
            continue
        #如果对应的index为TP_INDEX，则直接在TP_INDEX再添加一个重合的beat boundary：
        elif index == TP_INDEX:
            TP_BEAT.insert(TP_INDEX+1,TP_BEAT[TP_INDEX])
            SP_INDEX += 1
            TP_INDEX += 1
            continue
        #该种情况下，sp只走了一个beat而tp走了多个beat，可以考虑将这部分多的beat直接删除，也可以考虑视情况保留：
        else:
            for delete in range(index-TP_INDEX-1):
                TP_BEAT.pop(TP_INDEX+1)
            SP_INDEX += 1
            TP_INDEX += 1
            continue
    
    #在SP_INDEX+1的match结果里没有与之对应的beat boundary，则向后检测，直到找到能有对应值的SP_INDEX+N:
    #index==None的情况：
    else:
        N = 2
        while index == None and (SP_INDEX+N) < len(SP_BEAT):
            temp_index = BC.binary_search(MATCH1,float(SP_BEAT[SP_INDEX+N]))
            index = BC.binary_search( TP_BEAT, float(MATCH[temp_index][1]))
            N += 1 
        print(index-TP_INDEX,N-1)
        Comp_End = float(TP_BEAT[index])
        if index-TP_INDEX != N-1:
            #当SP与TP相隔beat数不相等时，以match结果为准
            #先删除掉beat检测的结果：
            for m in range(1,index-TP_INDEX):
                TP_BEAT.pop(TP_INDEX+1)
            
            for n in range(1,N-1):            
                Comp_Start = float(TP_BEAT[TP_INDEX+n-1])
                end = Comp_Start + 0.2
                MaxComp = 0
                MaxBoundary = Comp_Start
                while end < Comp_End:
                    Comp = LCS.lcs(SP_BEAT[SP_INDEX+n-1], SP_BEAT[SP_INDEX+n],Comp_Start,end)
                    end += 0.2
                    MaxComp = max(MaxComp,Comp)
                    if MaxComp == Comp:                       
                        MaxBoundary = end
                TP_BEAT.insert(TP_INDEX+n,str(MaxBoundary))

                #再将match的boundary添加进来：
#            for n in range(1,N-1):
#                temp_index = BC.binary_search(MATCH1,float(SP_BEAT[SP_INDEX+n]))
#                TP_BEAT.insert(TP_INDEX+n,MATCH[temp_index][1])
            SP_INDEX += N-1
            TP_INDEX += N-1
            continue
        else:
            #当SP与TP相隔beat数相等时，比较两者的匹配度Comp，以匹配度高者为新的boundary：
            for p in range(N-2):
                temp_index = BC.binary_search(MATCH1,float(SP_BEAT[SP_INDEX+p+1]))
                Comp_Match = LCS.lcs( SP_BEAT[SP_INDEX], SP_BEAT[SP_INDEX+p+1], TP_BEAT[TP_INDEX], MATCH[temp_index][1] )              
                Comp_Beat = LCS.lcs( SP_BEAT[SP_INDEX], SP_BEAT[SP_INDEX+p+1], TP_BEAT[TP_INDEX], TP_BEAT[TP_INDEX+p+1] )
                #MaxComp = MC.max_comparasion(Comp_Match,Comp_Beat)
                if Comp_Match > Comp_Beat:
                    #match结果更为准确
                    TP_BEAT.pop(TP_INDEX+p+1)
                    TP_BEAT.insert(TP_INDEX+p+1,MATCH[temp_index][1])
                else:
                    #beat原来的结果更为准确
                    continue 
            SP_INDEX += N-1
            TP_INDEX += N-1
            continue
        
    # Congratulations! You have reached the bottom of this loop!
                   
   
    
"""
Section 3: Output 
"""  

#填充  MATCH_BEAT:  
for i in range(len(TP_BEAT)):
    MATCH_BEAT.append(SP_BEAT[i].strip('\n')+','+TP_BEAT[i])
print(len(TP_BEAT),len(MATCH_BEAT))  
#将修正后的TP_BEAT文件保存为TP_BEAT.csv:

with open("TP_BEAT_correction_C.csv","w") as g:
    for line in TP_BEAT:
        g.write(line.strip()+"\n")

print('修正后的TP_BEAT文件保存为TP_BEAT_correction_C.csv','\n')

#将SP_BEAT与TP_BEAT的对应关系保存为MATCH_BEAT.csv:

with open("MATCH_BEAT_C.csv","w") as h:
    for item in MATCH_BEAT:
        h.write(item.strip()+"\n")
    
print('SP_BEAT与TP_BEAT的对应关系保存为MATCH_BEAT_C.csv','\n')

#打印程序运行时间：       
time_elapsed = time.clock()-time_start
print("Time consumed in this Program: ",time_elapsed,'\n')        
        
        