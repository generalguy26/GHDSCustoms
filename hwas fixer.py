# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 20:14:44 2020

@author: generalguy26
"""


hwas = open("song.hwas", "rb")

e = bytearray(hwas.read())

filesize = len(e)
b = bytearray(b'\xF0\x77\x77\xFF')

for x in range(0x200, filesize, 0x8000):
    e[x-1:x-1] = b #stackoverflow pls
    
out = open("newsong.hwas", "wb")
out.write(e)
hwas.close()
out.close()
