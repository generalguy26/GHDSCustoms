# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 16:41:39 2020

@author: generalguy26
"""


data = None

#hwas info taken from scorehero https://www.scorehero.com/forum/viewtopic.php?t=106685
#HWAS Header (0x200 / 512 bytes)
#- - - - - - - - - - - - - - - - - - - - - - -
#0x0 - "sawh" - "hwas" in little endian
#0x4 - Memory Allocation Length (always 32768, explanation later)
#0x8 - Sample Rate (always 19996)
#0xC - # of Channels (always 1, it is a mono track)
#0x10 - Loop Start Sample (always 0, offset from the start of the data section)
#0x14 - # of Samples (length of data portion, in bytes)
#0x18 - Loop End Sample (end of music, offset from the start of the data section)
#0x1C - 0s until end of header
#
#HWAS DATA Chunks
#- - - - - - - - - - - - - -
#These repeat until the end of the file:
#4 bytes - Unknown extra 4 bytes (Predictor/Step Index [affects the volume], least significant nibble always zero?)
#32764 bytes - Raw IMA ADPCM Data
#(Note: The last chunk of bytes does not have to be the full 32768 bytes)
#
#Note: An HWAS file ends on an even 0x200 block, so dummy data (like 00's or FF's or 88's) will need to fill the rest of the space.

with open('song.ima', 'rb') as song:                         #open ima adpcm encoded audio file
    

    #this part deprecates hwas fixer
    e = bytearray(song.read())                               # load data into bytearray
    #static header is deprecated
    #b = bytearray(b'\xF0\x77\x77\xFF')                       # set static header (deprecated)
    #for x in range(0x00, len(e), 0x8000):                    # insert every 0x8000 bytes (for some reason I don't see these bytes in the hex data but it still sounds okish???)
    #    e[x-1:x-1] = b                                       # insert these 4 bytes
    data = e

lastsample = len(data)                                       # mark location of last sample
padsize = 511 - (lastsample + 511) % 512                     # same thing as the chart compression padding, except this time filesize needs to be divisible by 512
bytepad = b'\x00' * padsize

size = lastsample + padsize
hwasheader = b'\x73\x61\x77\x68\x00\x80\x00\x00\x1C\x4E\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00' + size.to_bytes(4, 'little') + lastsample.to_bytes(4, 'little') + (b'\x00' * 0x1E4)

with open('song.hwas', 'wb+') as out:                        # create and write out hwas file
    out.write(hwasheader + data + bytepad)
