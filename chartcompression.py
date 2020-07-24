# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:55:52 2020

@author: generalguy26
"""


from ndspy import lz10 #nds uses lz10 compression for the chart files, ghds adds an extra 8 byte header to it

data = None #initialization

with open('chart.qgm', 'rb') as uncompressed:
    data = uncompressed.read() #read qgm chart data
    data = lz10.compress(data) # compress qgm chart data with ndspy
    

size = len(data)
padsize = 3 - (size + 3) % 4 #math to determine how many zeros to pad the end of the file with, filesize must be divisible by 4
size += padsize
bytepad = b'\x00' * padsize
magic = b'\x4C\x08\x00\x00\x45' + (size + 8).to_bytes(3, 'little') #creating the 8 byte header to prepend the compressed chart data with

with open('chart.lz77', 'wb+') as compressed:
    compressed.write(magic + data + bytepad) #write compressed data with 8 byte header and padding to new file
