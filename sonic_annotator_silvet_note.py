#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 17:01:42 2019

@author: alex
"""

import os
def rundata():
    os.system("/Users/alex/Desktop/ppaa/sonic-annotator -t /Users/alex/Desktop/ppaa/tp_pitch_active_fast.txt -m /Users/alex/Desktop/ppaa/sp_cut.wav -w csv --csv-basedir /Users/alex/Desktop/ppaa/data/")
    # os.system("/usr/bin/sonic-annotator                    -t /home/sunlf/programs/scripts/configs/tp_match_sp.txt -m /home/sunlf/tmp/wavs/tp.wav        /home/sunlf/tmp/wavs/1/sp.wav -w csv --csv-basedir      /home/sunlf/tmp/output/csvs")

    # os.system("/Users/jiating/Desktop/ppaa/sonic-annotator -t /Users/jiating/Desktop/ppaa/tp_onset_method_1.txt /Users/jiating/Desktop/ppaa/tp.wav -w csv --csv-basedir /Users/jiating/Desktop//identify/data")
    # os.system("/Users/jiating/Desktop/ppaa/sonic-annotator -t /Users/jiating/Desktop/ppaa/tp_onset_method_2.txt /Users/jiating/Desktop/ppaa/tp.wav -w csv --csv-basedir /Users/jiating/Desktop//identify/data")
    # os.system("/Users/jiating/Desktop/ppaa/sonic-annotator -t /Users/jiating/Desktop/ppaa/tp_pitch_active_s.txt /Users/jiating/Desktop/ppaa/tp.wav -w csv --csv-basedir /Users/jiating/Desktop/identify/data")


if __name__ == '__main__':
    rundata()