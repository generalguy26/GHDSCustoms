# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 15:55:52 2020

@author: generalguy26
"""


from ndspy import lz10

data = None

with open('chart.qgm', 'rb') as uncompressed:
    data = uncompressed.read()
    data = lz10.compress(data)
    

size = len(data)
padsize = 3 - (size + 3) % 4 #fixes word size
size += padsize
bytepad = b'\x00' * padsize
magic = b'\x4C\x08\x00\x00\x45' + (size + 8).to_bytes(3, 'little')

with open('chart.lz77', 'wb+') as compressed:
    compressed.write(magic + data + bytepad)
