#!/usr/bin/python3

# amplituda vyska
#frekvence pozicia

import wave, sys, struct
import numpy as np
wav = wave.open(sys.argv[1])
print(wav.getparams())
# print(struct.unpack('<h',wav.readframes(1)))
# input()
print(wav.getnframes()/100)
# input()
samp = 0
lst = []
maxs = []
mins = []
number = 0
for _ in range(wav.getnframes()):
    lst.append(struct.unpack('=h',wav.readframes(1))[0])
    samp += 1
    if samp == 100:
        number+=1
        print(number)
        samp = 0
        # print(lst)
        # print("---")
        lst_fft = np.fft.rfft(lst)
        # print(lst_fft)
        # print("---")
        lst_fft_abs = np.abs(lst_fft)
        # print(lst_fft_abs)
        # print("---")
        minn = min(lst_fft_abs)
        maxx = max(lst_fft_abs)
        avg = np.average(lst_fft_abs)
        if maxx >= 20*avg:
            maxs.append(maxx)
        if minn <= 20*avg: # takto asi nie, TODO zistit co je peak low
            mins.append(minn)
        
print(min(mins))
print(max(maxs))