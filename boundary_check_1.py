#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Header :
    
This program is used to detect if the matching boundary overlaps with a beat boundary in tp 
with the help of binary search algorithm.

@author: alex
"""

#二分法查找,返回与检测值t对应的TP_index，或是最近元素的index，若是最近的元素与检测值相差超过0.05s， 则返回 None:  
def binary_search(array,t):
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

    if distance1 < distance2 and distance1 <= 0.05:
        return array.index(array[height])
    elif distance2 <= distance1 and distance2 <= 0.05:
        return array.index(array[low])
    else:
        return None
 









