"""
Header:

此程序利用sp中的beat信息和match中的一一对应关系向tp中做映射，得到tp的beat信息，并计算相应的余铉近似度。

"""

import numpy as np

"""
函数部分
"""
#余铉近似度函数
def cosdistance(s1,s2):
    # 下面是余弦距离计算公式
    # dist = np.dot(s1, s2) / (np.linalg.norm(s1) * np.linalg.norm(s2))
    #先将s1,s2中的元素都转化为float型：
    s1 = list(map(lambda x:np.float64(x),s1))
    s2 = list(map(lambda x:np.float64(x),s2))
    num = float(np.matmul(s1, s2))
    norm1 = np.linalg.norm(s1)
    norm2 = np.linalg.norm(s2)
    s = norm1 * norm2
    if norm1 == 0 and norm2 == 0:
        result = 1.0
    elif s == 0:
        result = 0
    else:
        result = num / s
    return result

#二分法查找,返回与检测值t对应的index，或是最近元素的index:  
def binary_search(array,t):
    t = float(t)
    low = 0
    height = len(array)-1
    while low <= height:
        mid = (low+height)//2
        
        if float(array[mid]) < t:
            low = mid+1

        elif float(array[mid]) > t:
            height = mid-1 

        else:
            return array.index(array[mid])
    
    distance1 = abs(float(array[height]) - t)
    try:
        distance2 = abs(float(array[low])-t)
    except IndexError:
        print('Has reached the end of this audio file!')
        return array.index(array[height])

    if distance1 < distance2:
        return array.index(array[height])
    elif distance2 <= distance1:
        return array.index(array[low])
    else:
        pass

"""
数据导入
"""    
#从csv导入match数据和sp的beat信息：
match = []
with open("match.csv","r") as f:
    for line in f.readlines():
        match.append(line.strip('\n').split(','))
match_sp = []
for i in range(len(match)):
    match_sp.append(match[i][0])
sp_beat = []
with open("sp_beat.csv","r") as g:
    for line in g.readlines():
        sp_beat.append(line.strip('\n'))

#从silvet_pitchactivation.csv导入sp和tp的单音信息，用于余铉近似度计算：
sp_note = []
with open ("sp_silvet_pitchactivation.csv","r") as f1:
    for line in f1.readlines():
        sp_note.append(line.strip().split(','))
sp_note_time = []
for i in range(len(sp_note)):
    sp_note_time.append(sp_note[i][0])
    
tp_note = []
with open ("tp_silvet_pitchactivation.csv","r") as f2:
    for line in f2.readlines():
        tp_note.append(line.strip().split(','))   
tp_note_time = []
for i in range(len(tp_note)):
    tp_note_time.append(tp_note[i][0])
    
"""
beat映射
"""
#利用sp中的beat信息和match关系向tp中做映射，得到tp的beat信息：
tp_beat = []
for item in sp_beat:
    sp_index = binary_search(match_sp,item)
    tp_beat.append(match[sp_index][1])

#求近似度：
similarity = []
for i in range(len(tp_beat)):
    sp_index = binary_search(sp_note_time,sp_beat[i])
    tp_index = binary_search(tp_note_time,tp_beat[i])
    s1 = sp_note[sp_index][1:]
    s2 = tp_note[tp_index][1:]
    sim = cosdistance(s1,s2)
    similarity.append(sim)
    
for j in range(len(tp_beat)):
    tp_beat[j] = str(sp_beat[j])+','+str(tp_beat[j])+','+str(similarity[j])
    
#保存tp_beat.csv:
with open("tp_beat_match.csv","w") as h:
    for line in tp_beat:
        h.write(line+"\n")



    

