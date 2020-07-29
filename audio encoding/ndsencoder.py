# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 18:44:13 2020

@author: generalguy26
"""

#nds audio info can be found at https://www.akkit.org/info/gbatek.htm


import audioread
import struct
import codec

with audioread.audio_open('song.wav') as f: #audioread has little endian pcm16 values
    state = None
    data = b''
    pcm16 = 0
    headercounter = -4
    blocksize = 0x8000 - 16
    for buf in f: #buf is a 2048 byte buffer, we need to get the 16 bit (2 byte) pcm16 values from this
        for i in range(int(len(buf) / 4)): #loop through the buffer
            
            m = i * 4 #account for the division before
            headercounter += 4 #tracking how long it has been since a header has been inserted
            if headercounter % blocksize == 0: #header needs to be present at the beginning of every 0x8000 byte block, this checks if a header needs to be inserted
                headercounter = 0 #reset the tracker
                result = codec._calc_head(buf[m: m + 2]) #create the header
                print(result)
                data += result #insert the header to the bytes (apparently it doesn't really work and only inserts correctly at the beginning)
            pcm16 = buf[m : m + 2] #get first pcm16 value
            pcm16 = struct.unpack( '<h', pcm16)[0] #read as little endian short
            pcm162 = buf[m + 1 : m + 3] #get second pcm16 value
            pcm162 = struct.unpack( '<h', pcm162)[0] #read as little endian short
            sample = codec._encode_sample(pcm16) #calculate adpcm value for first pcm16 value
            sample2 = codec._encode_sample(pcm162) #calculate adpcm value for second pcm16 value
            print(sample, sample2)
            data += struct.pack('B', (sample2 << 4) | sample) #assemble values into a byte and append them to the datastream

with open('audio.ima', 'wb+') as w:
    w.write(data) #write datastream to file