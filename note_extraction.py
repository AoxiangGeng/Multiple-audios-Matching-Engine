
"""
Header :
    
This Program is used to extract Note information ( Which note occurs at a given time point ) 
from the output of Silvet-pitch-activation Transform. The result is saved as pitch_active.csv,
in which, every row consists of a time point at column 1 and the corresponding note sequence in the rest of columns 

@author: alex
"""
import csv
import json

def note_extraction(filename):
    #给定pitch template：
    pitchlist = ['A0', 'A#0', 'B0', 'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6', 'C7', 'C#7', 'D7', 'D#7', 'E7', 'F7', 'F#7', 'G7', 'G#7', 'A7', 'A#7', 'B7', 'C8']
             
    #打开Silvet pitch-activation Transform 导出的结果，转换成pitch信息并将其保存为字典 dic：
    with open(filename+".csv","r") as f:
        l1 = []
        for line in f.readlines():
            l2 = line.strip().split(",")
            a = 0
            for item in l2[1:]:
                a += float(item)
                #剔除空白部分
                if a != 0:
                    l1.append(l2)

    dic = {}
    for line in range(len(l1)):
        #l1[line][0]处为时间
        dic[l1[line][0]] = []
        for item in range(len(l1[line][1:])):
            if l1[line][item+1] != "0":
            
                dic[l1[line][0]].append(pitchlist[item])
    #让dic的第一列（时间序列）以时间顺序排列：
    datas = sorted(dic.items(), key=lambda v: float(v[0]))


    #将结果以字典的形式保存为相应的pitch_active.csv:
    with open(filename+"_pitch_active.csv","w") as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['time_point','pitch_names'])
        #写入列标题，即DictWriter构造方法的fieldnames参数
        writer.writeheader()
        for data in datas:
            #注意！！！写csv只能写成str格式，要想保留原来的list格式，必须引用json， 用json.dumps存储， 用json.loads读取：
            writer.writerow({'time_point':data[0],'pitch_names':json.dumps(data[1])})


file1 = "sp_cut_note"
file2 = "tp_cut_note"
note_extraction(file1)
note_extraction(file2)
"""
with open("pitch_active.csv","w") as f:
    for line in data:
        l1 = ','.join(line[1])
        f.write(line[0]+','+l1+"\n")

#第一列为时间序列，每一行除第一列剩余的元素表示该时间点所对应的单音s.
"""


