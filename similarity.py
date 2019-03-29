import numpy as np
import itertools as it
from numpy import array, zeros, full, argmin, inf, ndim
from math import isinf
import json
from fastdtw import fastdtw


class CosineMatch():
    def __init__(self,datalist):
        self.datalist = datalist
        self.spstartpoint = self.datalist[0] / 0.02 + 1
        self.spendpoint = self.datalist[1] / 0.02 + 1
        self.tpstartpoint = self.datalist[2] / 0.02 + 1
        self.tpendpoint = self.datalist[3] / 0.02 + 1

    def __dealcsv(self,spstart,spend,tpstart,tpend):
        """根据datalist列表从csv文件中读取到数据"""
        splist = []
        spreadnum = 1
        with open("./sp_cut_note.csv","r") as f:
            for line in f.readlines():
                if spreadnum>=spstart and spreadnum<=spend:
                    smallsplist = list(map(lambda x:np.float64(x),line.strip("\n").split(",")))
                    splist.append(smallsplist[1:])
                    if spreadnum == spend:
                        break
                spreadnum += 1
        tplist = []
        tpreadnum = 1
        with open("./tp_cut_note.csv","r") as f:
            for line in f.readlines():
                if tpreadnum >=tpstart and tpreadnum<=tpend:
                    smalltplist = list(map(lambda x:np.float64(x),line.strip("\n").split(",")))
                    tplist.append(smalltplist[1:])
                    if tpreadnum == tpend:
                        break
                tpreadnum += 1
        return splist,tplist

    def cosdistance(self,s1,s2):
        """求两个一维向量的余弦相似度"""
        # 下面是余弦距离计算公式，现在暂时还用不到
        # dist1 = 1 - np.dot(s1, s2) / (np.linalg.norm(s1) * np.linalg.norm(s2))
        num = float(np.matmul(s1, s2))
        s = np.linalg.norm(s1) * np.linalg.norm(s2)
        if s == 0:
            result = 1.0
        else:
            result = 1.0 - num / s
        return result

    def calmatchpoint(self):
        """计算sp中所有点到tp所有点的余弦距离"""
        splist,tplist = self.__dealcsv(self.spstartpoint,self.spendpoint,self.tpstartpoint,self.tpendpoint)
        allspmatchtp = []
        print(splist[0])
        print(tplist[0])
        for sppoint in splist:
            spmatchtp = [self.cosdistance(sppoint[1:],tppoint[1:]) for tppoint in tplist]
            allspmatchtp.append(spmatchtp)
        return allspmatchtp

    def findmatchpoint(self):

        """通过穷举法搜索两次，找到match最接近的点"""
        splist, tplist = self.__dealcsv(self.spstartpoint, self.spendpoint, self.tpstartpoint, self.tpendpoint)
        spnum = len(splist)
        tpnum = len(tplist)
        maxdiscoslist = [[],[],0]
        i = min(spnum,tpnum)
        circlenum = 0
        while circlenum<2:
            spindexlist = list(it.combinations(range(0,spnum),i))
            tpindexlist = list(it.combinations(range(0,tpnum),i))
            for sppoint in spindexlist:
                for tppoint in tpindexlist:
                    discos = 0
                    for j in range(len(sppoint)):
                        discos += self.cosdistance(splist[sppoint[j]],tplist[tppoint[j]])
                    if discos > maxdiscoslist[2]:
                        # print(maxdiscoslist)
                        maxdiscoslist[0] = sppoint
                        maxdiscoslist[1] = tppoint
                        maxdiscoslist[2] = discos
            # print(maxdiscoslist)
            i -= 1
            circlenum += 1
        with open("sp_match_tp.csv","a")as f:
            for i in range(len(maxdiscoslist[0])):
                f.write("%.2f" % (maxdiscoslist[0][i]*0.02 + self.datalist[0]) + ","\
                        +"%.2f" % (maxdiscoslist[1][i]*0.02 + self.datalist[2])+"\n")
        return maxdiscoslist

    def _traceback(self,D):
        """追溯最短路径，并返回对应数组"""
        i, j = array(D.shape) - 2
        inum = len(D)
        jnum = len(D[0])
        p, q = [i], [j]
        while (i > 0) or (j > 0):
            if i<0 and abs(i)>inum:
                i = -inum
            if j<0 and abs(j)>jnum:
                j = -jnum
            print(i)
            print(j)
            print("------")
            tb = argmin((D[i, j], D[i, j + 1], D[i + 1, j]))
            if tb == 0:
                i -= 1
                j -= 1
            elif tb == 1:
                i -= 1
            else:  # (tb == 2):
                j -= 1
            p.insert(0, i)
            q.insert(0, j)
        return array(p), array(q)

    def dtw(self, warp=1, w=inf, s=1.0):
        """dtw算法计算最短路径"""
        y, x = self.__dealcsv(self.spstartpoint, self.spendpoint, self.tpstartpoint, self.tpendpoint)
        assert len(x)
        assert len(y)
        assert isinf(w) or (w >= abs(len(x) - len(y)))
        assert s > 0
        r, c = len(x), len(y)
        if not isinf(w):
            D0 = full((r + 1, c + 1), inf)
            for i in range(1, r + 1):
                D0[i, max(1, i - w):min(c + 1, i + w + 1)] = 0
            D0[0, 0] = 0
        else:
            D0 = zeros((r + 1, c + 1))
            D0[0, 1:] = inf
            D0[1:, 0] = inf
        D1 = D0[1:, 1:]  # view
        for i in range(r):
            for j in range(c):
                if (isinf(w) or (max(0, i - w) <= j <= min(c, i + w))):
                    D1[i, j] = self.cosdistance(x[i], y[j])
        C = D1.copy()
        jrange = range(c)
        for i in range(r):
            if not isinf(w):
                jrange = range(max(0, i - w), min(c, i + w + 1))
            for j in jrange:
                min_list = [D0[i, j]]
                for k in range(1, warp + 1):
                    i_k = min(i + k, r)
                    j_k = min(j + k, c)
                    min_list += [D0[i_k, j] * s, D0[i, j_k] * s]
                D1[i, j] += min(min_list)
        if len(x) == 1:
            path = zeros(len(y)), range(len(y))
        elif len(y) == 1:
            path = range(len(x)), zeros(len(x))
        else:
            path = self._traceback(D0)
        tp,sp = path
        with open("sp_dtwmatch_tp.csv","a")as f:
            for i in range(len(sp)):
                if i == 0:
                    f.write("%.2f" % (sp[i]*0.02 + self.datalist[0])+","+"%.2f"%(tp[i]*0.02 + self.datalist[2]) + "\n")
                else:
                    if sp[i] != sp[i-1]:
                        f.write("%.2f" % (sp[i] * 0.02 + self.datalist[0]) + "," + "%.2f" % (
                        tp[i] * 0.02 + self.datalist[2]) + "\n")
        return D1[-1, -1] / sum(D1.shape), C, D1, path

    def fast_dtw(self):
        """用fastdtw计算最短路径"""
        y, x = self.__dealcsv(self.spstartpoint, self.spendpoint, self.tpstartpoint, self.tpendpoint)
        distance, path = fastdtw(x, y, dist=self.cosdistance)
        print(path)
        with open("sp_fastdtwmatchcos_tp2.csv","a")as f:
            for i in range(len(path)):
                f.write("%.2f" % (path[i][0]*0.02 + self.datalist[2])+","+"%.2f"%(path[i][1]*0.02 + self.datalist[0]) + "\n")
        return distance,path

if __name__ == '__main__':
    w = inf
    s = 1.0
    p = 1
    with open("temp_match_7.csv","r")as f:
        for line in f.readlines():
            print(p)
            matchtimepoint = list(map(lambda x:float(x),list(json.loads(line.strip('\n')))))
            dislist = CosineMatch(matchtimepoint)
            dislist.fast_dtw()
            p += 1



