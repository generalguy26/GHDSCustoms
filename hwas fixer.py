#this file is completely deprecated now, do not use this

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 20:14:44 2020

@author: generalguy26
"""
#this file is largely deprecated unless you are manually going through all the steps to convert for some reason

hwas = open("song.hwas", "rb")

e = bytearray(hwas.read()) #open hex code of hwas

filesize = len(e)
b = bytearray(b'\xF0\x77\x77\xFF') #define arbitrary 4 byte predictor for ima adpcm

for x in range(0x200, filesize, 0x8000): #insert these 4 bytes every 0x8000 bytes (block size of samples it predicts)
    e[x-1:x-1] = b #insertion code I took from stackoverflow
    
out = open("newsong.hwas", "wb") #writing data to new hwas file
out.write(e)
hwas.close()
out.close()
