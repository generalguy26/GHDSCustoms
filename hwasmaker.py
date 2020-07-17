# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:41:39 2020

@author: removevirus
"""


data = None

with open('song.ima', 'rb') as song:
    

    #this part deprecates hwas fixer
    e = bytearray(song.read())
    b = bytearray(b'\xF0\x77\x77\xFF')
    for x in range(0x00, len(e), 0x8000):
        e[x-1:x-1] = b #stackoverflow pls
    data = e

lastsample = len(data)
padsize = 511 - (lastsample + 511) % 512 #fixes word size
bytepad = b'\x00' * padsize

size = lastsample + padsize
hwasheader = b'\x73\x61\x77\x68\x00\x80\x00\x00\x1C\x4E\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00' + size.to_bytes(4, 'little') + lastsample.to_bytes(4, 'little') + (b'\x00' * 0x1E4)

with open('song.hwas', 'wb+') as out:
    out.write(hwasheader + data + bytepad)