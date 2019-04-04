"""
Header:

此程序利用sp中的beat信息和match中的一一对应关系向tp中做映射，得到tp的beat信息，并计算相应的近似度。

"""

import numpy as np
import math
import LCS as LCS

class Beat_Mapping():
    """此类利用sp中的beat信息和match中的一一对应关系向tp中做映射，
    得到tp的beat信息，并计算相应的余铉近似度。"""
    def __init__(self, old_match, new_match, sp_beat, sp_note, tp_note, save_directory):
    # 数据导入：
        self.old_match = old_match
        self.new_match = new_match
        self.sp_beat = sp_beat
        self.sp_note = sp_note
        self.tp_note = tp_note
        self.save_directory = save_directory
        self.old_match_sp = []
        self.new_match_sp = []
        self.tp_note_time = []
        self.sp_note_time = []
        self.old_match, self.old_match_sp, self.new_match, self.new_match_sp, self.sp_beat, self.sp_note,self.sp_note_time, self.tp_note, self.tp_note_time = self.data_import(self.old_match, self.new_match, self.sp_beat,self.sp_note, self.tp_note)
        # 参数初始化：
        self.tp_beat_old = []
        self.tp_beat_new = []
        self.similarity_old = [0.0]
        self.similarity_new = [0.0]
        self.tp_beat = []
        self.mark = []
        # 指定保存地址：/path/to/save/filename
        self.save_path = save_directory

    def mapping(self):
        """主体映射函数 """
        # beat初步映射：
        for item in self.sp_beat:
            sp_index = self.binary_search(self.old_match_sp, item)
            self.tp_beat_old.append(self.old_match[sp_index][1])

        for item in self.sp_beat:
            sp_index = self.binary_search(self.new_match_sp, item)
            self.tp_beat_new.append(self.new_match[sp_index][1])

        # 判断两个match的映射结果是否存在相同之处，相同的标记为1，否则为0:
        for i in range(len(self.tp_beat_old)):
            mean = 0.0
            if i == 0:
                self.tp_beat.append(float(self.tp_beat_new[0]))
                self.mark.append(1)
            else:
                if abs(float(self.tp_beat_new[i]) - float(self.tp_beat_old[i])) <= 0.1:
                    self.tp_beat.append(float(self.tp_beat_new[i]))
                    self.mark.append(1)
                else:
                    # 根据LCS算法求当前beat单元的近似度：
                    sp_start = self.sp_beat[i - 1]
                    sp_end = self.sp_beat[i]
                    tp_start = self.tp_beat[i - 1]
                    tp_new_end = self.tp_beat_new[i]
                    tp_old_end = self.tp_beat_old[i]
                    identity_old1 = LCS.lcs(sp_start, sp_end, tp_start, tp_old_end,self.save_directory+"/sp_note.csv",self.save_directory+"/tp_note.csv")
                    identity_new1 = LCS.lcs(sp_start, sp_end, tp_start, tp_new_end,self.save_directory+"/sp_note.csv",self.save_directory+"/tp_note.csv")
                    # 计算当前beat单元的gap，并和之前10个beat单元的平均gap值作比较，得出一个identity：
                    if i <= 10:
                        if identity_new1 >= identity_old1:
                            self.tp_beat.append(self.tp_beat_new[i])
                            self.mark.append(1)
                        else:
                            self.tp_beat.append(self.tp_beat_old[i])
                            self.mark.append(1)
                    else:
                        mean = (float(self.tp_beat[i - 1]) - float(self.tp_beat[i - 11])) / 10
                        gap_old = float(self.tp_beat_old[i]) - float(self.tp_beat[i - 1])
                        gap_new = float(self.tp_beat_new[i]) - float(self.tp_beat[i - 1])
                        identity_old2 = (1 - abs(mean - gap_old) / mean) * 100 / 3
                        identity_new2 = (1 - abs(mean - gap_new) / mean) * 100 / 3
                        identity_old = identity_old1 + identity_old2
                        identity_new = identity_new1 + identity_new2
                    # print(i, identity_new1, identity_new2, identity_old1, identity_old2)
                    # 执行判断，取identity高者的beat时间为最终结果：
                        if identity_new >= identity_old:
                            self.tp_beat.append(self.tp_beat_new[i])
                            if identity_new > 28.0:
                                self.mark.append(1)
                            else:
                                self.mark.append(0)
                        else:
                            self.tp_beat.append(self.tp_beat_old[i])
                            if identity_old > 28.0:
                                self.mark.append(1)
                            else:
                                self.mark.append(0)
        return self.tp_beat
    
    def save_output(self):
        """保存"""
        #保存tp_beat.csv
        with open(self.save_path+"/tp_beat.csv","w") as h1:
            for i in range(len(self.tp_beat)):
                h1.write(str(self.tp_beat[i])+","+str(self.mark[i])+"\n")
        #保存new_match.csv
        # with open(self.save_path+"/match.csv","w") as h2:
        #     for line in self.tp_beat:
        #         h2.write(str(line)+"\n")
        
    def data_import(self,filename_old_match,filename_new_match,filename_sp_beat,filename_sp_note,filename_tp_note):
        """从临时文件保存路径读取所需的csv文件：old_match,new_match,sp_beat,sp_note,tp_note """
        #从csv导入 old match数据：
        match_old = []
        with open(filename_old_match,"r") as f:
            for line in f.readlines():
                match_old.append(line.strip('\n').split(','))
        #将第一列sp的时间数据分别保存，方便之后的二分法查找：       
        match_old_sp = []
        for i in range(len(match_old)):
            match_old_sp.append(match_old[i][0])
        #从csv导入 old match数据：     
        match_new = []
        with open(filename_new_match,"r") as f:
            for line in f.readlines():
                match_new.append(line.strip('\n').split(','))
        #将第一列sp的时间数据分别保存，方便之后的二分法查找：          
        match_new_sp = []
        for i in range(len(match_new)):
            match_new_sp.append(match_new[i][0])
        #从csv导入 sp的beat数据：   
        sp_beat = []
        with open(filename_sp_beat,"r") as g:
            for line in g.readlines():
                sp_beat.append(line.strip('\n'))        
        #从silvet_pitchactivation.csv导入sp经过note_extraction处理过的单音信息，用于近似度计算：
        sp_note = []
        with open (filename_sp_note,"r") as f1:
            for line in f1.readlines():
                sp_note.append(line.strip().split(','))
        #将第一列sp的时间数据分别保存，方便之后的二分法查找：        
        sp_note_time = []
        for i in range(len(sp_note)):
            sp_note_time.append(sp_note[i][0])  
        #从silvet_pitchactivation.csv导入sp经过note_extraction处理过的单音信息，用于近似度计算：    
        tp_note = []
        with open (filename_tp_note,"r") as f2:
            for line in f2.readlines():
                tp_note.append(line.strip().split(','))   
        #将第一列tp的时间数据分别保存，方便之后的二分法查找：        
        tp_note_time = []
        for i in range(len(tp_note)):
            tp_note_time.append(tp_note[i][0])
        #返回list
        return match_old, match_old_sp, match_new, match_new_sp, sp_beat, sp_note, sp_note_time, tp_note, tp_note_time 
    
    def cosdistance(self,s1,s2):
        """余铉近似度函数"""
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

    def Euclidean(self,s1,s2):
        """欧式距离计算函数"""
        s1 = list(map(lambda x:np.float64(x),s1))
        s2 = list(map(lambda x:np.float64(x),s2))
        s1 = np.array(s1)
        s2 = np.array(s2)
        distance=np.sqrt(np.sum(np.square(s1-s2)))
        return distance
    
    def pearson(self,vector1, vector2):
        """Pearson距离计算函数"""
        n = len(vector1)
        vector1 = list(map(lambda x:np.float64(x),vector1))
        vector2 = list(map(lambda x:np.float64(x),vector2))
        #simple sums
        sum1 = sum(float(vector1[i]) for i in range(n))
        sum2 = sum(float(vector2[i]) for i in range(n))
        #sum up the squares
        sum1_pow = sum([pow(v, 2.0) for v in vector1])
        sum2_pow = sum([pow(v, 2.0) for v in vector2])
        #sum up the products
        p_sum = sum([vector1[i]*vector2[i] for i in range(n)])
        #分子num，分母den
        num = p_sum - (sum1*sum2/n)
        den = math.sqrt((sum1_pow-pow(sum1, 2)/n)*(sum2_pow-pow(sum2, 2)/n))
        if den == 0:
            return 0.0
        return num/den
    
    def binary_search(self,array,t):
        """二分法查找,返回与检测值t对应的index，或是最近元素的index""" 
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
        
    def binary_search_accurate(self,array,t):
        """精准二分法查找,若在检测值t附近存在对应值，返回True，否则返回False，要求偏差小于0.05""" 
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
                return True    
        distance1 = abs(float(array[height]) - t)
        try:
            distance2 = abs(float(array[low])-t)
        except IndexError:
            print('Has reached the end of this audio file!')
            return True
        if distance1 < distance2 and distance1 <= 0.05:
            return True
        elif distance2 <= distance1 and distance2 <= 0.05:
            return True
        else:
            return False
        
if __name__ == '__main__':
    beatm = Beat_Mapping("./match_old.csv","./match_new.csv","./sp_beat.csv","./sp_note.csv","./tp_note.csv","./")
    beatm.mapping()
    beatm.save_output()
    
    





    

