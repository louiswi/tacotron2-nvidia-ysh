import os
import wave
import contextlib
import sys

import matplotlib.pyplot as plt
import pprint



def read_duration(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
    return duration

# wav_path = sys.argv[1]
# wav_list = os.listdir(wav_path)
# wav_list = [wav for wav in wav_list if wav.endswith('wav')]
#
#
# durations = 0
# min_duration = 99999999
# max_duration = -1
# for wav in wav_list:
#         d = read_duration(f'{wav_path}/{wav}')
#         durations += d
#         min_duration = d if d < min_duration else min_duration
#         max_duration = d if d > max_duration else max_duration


# print('wav clips len:',len(wav_list))
# print('total duration(h)', durations/3600)
# print('avg duration(s)', (durations/float(len(wav_list))))
# print('min duration(s)', min_duration)
# print('max duration(s)', max_duration)


# txt = '/raid1/stephen/data/new_annotation_0307/metadata.csv'
# txt = '/raid1/stephen/data/new_annotation_0307/metadata_clip_1_10.csv'
# txt = '/raid1/stephen/data/new_annotation_0307/metadata_clip_dur1to10_ratio0.04to0.3.csv'
txt = '/raid1/stephen/data/ysh_annotation/metadata.csv'


# txtw = '/raid1/stephen/data/new_annotation_0307/metadata_clip_dur1to10_ratio0.04to0.3.csv'


f = open(txt, 'r')
# fw = open(txtw, 'w', encoding='utf-8')
lines = f.readlines()

res = []
for line in lines:
    wav_path = line.split('|')[0]
    text = line.split('|')[1]
    len_text = len(text)
    duration = read_duration('/raid1/stephen/data/ysh_annotation/wavs/'+wav_path+'.wav')
    # duration = read_duration(wav_path)
    ratio = duration/len_text
    res.append((wav_path ,duration, ratio))

    #clip with duration
    if duration>10 or duration < 1:
        continue

    #clip with ratio
    if ratio>0.3 or ratio < 0.05:
        continue
    # fw.write(line)
durations = [item[1] for item in res]
print('durtions:')
print(max(durations))
print(min(durations))
print(sum(durations)/len(durations))
print('\n')





# print(len([duration for duration in durations if duration>100]))

ratios = [item[2] for item in res]
print('ratios:')
print(max(ratios))
print(min(ratios))
print(sum(ratios)/len(ratios))

res = sorted(res, key=lambda x:x[-1])
pprint.pprint(res[:10])
# bad = [item for item in res if item[2]<0.04]
# print('\n')
# pprint.pprint(bad)


# An "interface" to matplotlib.axes.Axes.hist() method
n, bins, patches = plt.hist(x=ratios, range=[0,0.3])
plt.show()