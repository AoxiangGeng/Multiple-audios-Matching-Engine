import pretty_midi
import numpy as np
import csv
from mido import MidiFile
def get_beats(path,sub_path):
    Path = path+sub_path
    position = sub_path.find('.mid')
    new_sub_path = sub_path[:position]
    print(Path)
    denominators = []
    numerators = []
    indx = 0
    ticks = 0
    mid = MidiFile(Path)
    object_t = pretty_midi.PrettyMIDI(Path,resolution = 220,initial_tempo = 90.0)

    time_signatures = []
    track_number = 0
    for i, track in enumerate(mid.tracks):
        for j,msg in enumerate(track):
            if str(msg).find('numerator') > 1 :
                track_number = i
                break
    for i, track in enumerate(mid.tracks):
        if track_number == i :
            for j,msg in enumerate(track):
                if str(msg).find('velocity') > 1 :
                    vel = int(str(msg.velocity))
                    if i == 0 :
                        ticks += msg.time
                if str(msg).find('numerator') > 1 :
                    time_signatures.append(round(object_t.tick_to_time(ticks),4))
                    denominators.append(msg.denominator)
                    numerators.append(msg.numerator)
                if str(msg).find('message') > 1 and i==0 :
                    ticks += msg.time

    beats_ = object_t.get_beats(start_time = 0.0)
    beats = np.round(beats_,4)
    barlinetimestamp_ = object_t.get_downbeats(start_time=0)
    barlinetimestamp = np.round(barlinetimestamp_,4)
    beats_groups = []
    for i,measure in enumerate(barlinetimestamp[:-1]): # grouping beats based on measure
        beats_groups.append([])
        next_measure = barlinetimestamp[i+1]
        for one_beat in beats :
            if one_beat >= measure and one_beat < next_measure:
                beats_groups[i].append(one_beat)

    tempo_time_position = 0
    temp_denominator = denominators[0]
    temp_numerator = numerators[0]
    names = []
    normality = []
    Not_yet = 1
    if len(time_signatures) == 1 :
        Not_yet = 2
    for i,group in enumerate(beats_groups):
        if Not_yet == 1 :
            if group[0] > time_signatures[tempo_time_position+1] :
                tempo_time_position +=1
                temp_denominator = denominators[tempo_time_position]
                temp_numerator = numerators[tempo_time_position]
                if tempo_time_position == len(time_signatures) - 1 :
                    Not_yet = 2
        if len(group) == temp_numerator : # no error 
            for j,beat in enumerate(group):
                name = str(i+1)+'-'+str(j)+'/'+str(temp_denominator)
                names.append(name)
                normality.append('n')
        else : # error
            for j,beat in enumerate(group):
                name = str(i+1)+'-'+str(j)+'/'+str(temp_denominator)
                names.append(name)
                normality.append('e')

    onset_ = object_t.get_onsets()
    onset = np.round(onset_,4)
    result = []
    with open(str(str(path)+str(new_sub_path)+'_beats_from_midi'+'.csv'), 'w') as writeFile:
            writer = csv.writer(writeFile)
            for i in range(len(names)):
                beat = beats[i]
                if beat in onset : 
                    result.append([beat,str(names[i]),str(normality[i])])
                    row = [[beat,str(names[i]),str(normality[i])]]
                    writer.writerows(row)
            writeFile.close()
            
    return result

#test：
#a = get_beats('/Users/alex/Desktop/work/Test_madmom/match_test_data/sp1/','sp1.mid')
