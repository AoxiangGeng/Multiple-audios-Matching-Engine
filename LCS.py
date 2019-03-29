#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header :
    
This program illustrates a new comparasion algorithm -- LCS(longest common subsequence)
Given the input of time points(str): sp_start,sp_end,tp_start,tp_end. The program will
cut and extract the corresponding segment of pitch information from the original csv files,
then calculate the LCS (called as Symbol within) between sp and tp segments and compute the 
identity rate of LCS. Finally, return the identity rate and the index of this LCS in the
extracted tp segment.

Identity,Symbol,Index_LCS,time_tp = LCS(sp_start,sp_end,tp_start,tp_end)

Using time_tp[Index_LCS[i]], users can easily obtain the corresponding time point of each
LCS items. Specifically, one can use:  time_tp[Index_LCS[0]] and time_tp[Index_LCS[-1]] 
to locate this LCS in tp_pitch_active.csv (original csv file) for further division of tp.

@author: alex
"""

import csv
import json

"""
Section 1: Define the internal functions
"""    

#建立一个二维全零矩阵，矩阵的维度为输入的两个list的长度：
def zeros(shape):
    retval = []
    for x in range(shape[0]):
        retval.append([])
        for y in range(shape[1]):
            retval[-1].append(0)
    return retval

#制定积分规则：相等加十分，不相等扣五分，空格扣五分：
match_award      = 10
mismatch_penalty = -5
gap_penalty      = -5 # both for opening and extanding

#该函数用于计算每个单元格的分值：
def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

#该函数利用回溯的结果计算LCS和Identity rate：
def finalize(align1, align2):
    #划重点，这一句要考：
    align1 = align1[::-1]    #reverse sequence 1
    align2 = align2[::-1]    #reverse sequence 2
    #calcuate identity, score and aligned sequeces
    symbol = []
    INDEX_LCS = []
    #found = 0
    score = 0
    identity = 0

    #注意，此处的for循环意味着sequence1 的长度应等于或小于 sequence2 ！
    for i in range(0,len(align1)):
        # if two AAs are the same, then output the letter
        if align1[i] == align2[i]:                
            symbol.append(align1[i])
            INDEX_LCS.append(i)
            identity = identity + 1
            score += match_score(align1[i], align2[i])
    
        # if they are not identical and none of them is gap
        elif align1[i] != align2[i] and align1[i] != '-' and align2[i] != '-': 
            score += match_score(align1[i], align2[i])
            #symbol += ' '
            #found = 0
    
        #if one of them is a gap, output a space
        elif align1[i] == '-' or align2[i] == '-':          
            #symbol += ' '
            score += gap_penalty
    
    identity = (float(identity) / (len(align1)+len(align2)+1)) * 100
    
    print ('Identity =', "%3.3f" % identity, 'percent')

    return identity,symbol,INDEX_LCS


def needle(seq1, seq2):
    m, n = len(seq1), len(seq2)  # length of two sequences
    # Generate DP table and traceback path pointer matrix
    score = zeros((m+1, n+1))      # the DP table
    # Calculate DP table
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score[i - 1][j - 1] + match_score(seq1[i-1], seq2[j-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            score[i][j] = max(match, delete, insert)
    # Traceback and compute the alignment 
    #align1, align2 = '', ''
    align1, align2 = [], []
    i,j = m,n # start from the bottom right cell
    while i > 0 and j > 0: # end toching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]

        if score_current == score_diagonal + match_score(seq1[i-1], seq2[j-1]):
            align1.append(seq1[i-1])
            align2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1.append(seq1[i-1])
            align2.append('-')
            i -= 1
        elif score_current == score_up + gap_penalty:
            align1.append('-')
            align2.append(seq2[j-1])
            j -= 1

    # Finish tracing up to the top left cell
    while i > 0:
        align1.append(seq1[i-1])
        align2.append('-')
        i -= 1
    while j > 0:
        align1.append('-')
        align2.append(seq2[j-1])
        j -= 1
    
    print(len(align1),len(align2))
    identity,symbol,index_lcs = finalize(align1, align2)
    return identity

def water(seq1, seq2):
    m, n = len(seq1), len(seq2)  # length of two sequences
    
    # Generate DP table and traceback path pointer matrix
    score = zeros((m+1, n+1))      # the DP table
    pointer = zeros((m+1, n+1))    # to store the traceback path
    
    max_score = 0        # initial maximum score in DP table
    # Calculate DP table and mark pointers
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            score_diagonal = score[i-1][j-1] + match_score(seq1[i-1], seq2[j-1])
            score_up = score[i][j-1] + gap_penalty
            score_left = score[i-1][j] + gap_penalty
            score[i][j] = max(0,score_left, score_up, score_diagonal)
            if score[i][j] == 0:
                pointer[i][j] = 0 # 0 means end of the path
            if score[i][j] == score_left:
                pointer[i][j] = 1 # 1 means trace up
            if score[i][j] == score_up:
                pointer[i][j] = 2 # 2 means trace left
            if score[i][j] == score_diagonal:
                pointer[i][j] = 3 # 3 means trace diagonal
            if score[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = score[i][j];
    
    #align1, align2 = '', ''    # initial sequences
    align1, align2 = [], []
    i,j = max_i,max_j    # indices of path starting point
    
    #traceback, follow pointers
    while pointer[i][j] != 0:
        if pointer[i][j] == 3:
            align1.append(seq1[i-1])
            align2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif pointer[i][j] == 2:
            align1.append('-')
            align2.append(seq2[j-1])
            j -= 1
        elif pointer[i][j] == 1:
            align1.append(seq1[i-1])
            align2.append('-')
            i -= 1

    identity,symbol,index_lcs = finalize(align1, align2)
    return identity
    

"""
Section 2: Main body of this algorithm
"""

def lcs(sp_start,sp_end,tp_start,tp_end):
    
    #从原始csv文件截取所需片段导入单音信息，sp_start,sp_end,tp_start,tp_end
    with open('sp_cut_note_pitch_active.csv','r') as f:
        reader = csv.DictReader(f)
        list_sp = [json.loads(row['pitch_names']) for row in reader if float(row['time_point']) >= float(sp_start) and float(row['time_point']) <= float(sp_end)]  

    with open('tp_cut_note_pitch_active.csv','r') as h:
        reader = csv.DictReader(h)
        list_tp = [json.loads(row['pitch_names']) for row in reader if float(row['time_point']) >= float(tp_start) and float(row['time_point']) <= float(tp_end)]  
    #将相应片段的单音信息整合成一个字符串list--sp,tp：
    sp = []
    tp = []
    for lane in list_sp:
        sp += lane
    for lane in list_tp:
        tp += lane


    #以字典形式保留tp时间节点信息，使得时间信息和单音索引index一一对应，方便最后由最大公共子序列岁对应的单音index回溯找到其相应的发生时间：
    time_tp = {}
    temp = {}
    count = 0
    with open('tp_cut_note_pitch_active.csv','r') as h:
        reader = csv.DictReader(h)
        for row in reader:
            if float(row['time_point']) >= float(tp_start) and float(row['time_point']) <= float(tp_end):        
                temp[row['time_point']] = json.loads(row['pitch_names'])

    for time,pitch in temp.items():       
        index = [count+pitch.index(item) for item in pitch]
        count += len(pitch)
        for items in index: 
            time_tp[items] = time

    #利用Needleman-Wunsch算法求sp，tp的最大公共子序列：
    Identity = needle(sp,tp)
    #return Identity,Symbol,Index_LCS,time_tp
    return Identity


#test:
#Identity,Symbol,Index_LCS,time_tp = LCS(3,3.6,2,6.7)
#print(time_tp[Index_LCS[1]])



