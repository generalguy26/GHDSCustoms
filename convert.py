# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:44:09 2019
@author: generalguy26
"""

import chparse

def tickstoseconds(ticks, bpm):
    return ticks / 192 * 60 / bpm  #192 ticks per beat divided by beats per second
                                    #this is hardcoded to the resolution, may need to pull from metadata of the song
                                    #in the case of chiasm, original was at 480, but it's easier to reexport the chart with 192 res in moonscraper 
def tickstoms(ticks, bpm):
    return ticks / 192 * 60 / bpm * 1000
#%%Other Detection
        
def printchart(notes): #this is the best function in this entire script, feel free to call this
    for note in (notes[::-1]):
        notestring = '- - - - -'
        lns = list(notestring)
        for fret in note:
            lns[2 * fret] = 'O'
        print(''.join(lns))
        
#%% add notes to a dictionary cooresponding to their tick number, and group chords together
def getFretDict(chart):
    fretarray = {}
    for note in xg:
        try:
            if fretarray.get(note.time, -1) == -1:
                fretarray[note.time] = [note.fret]
            else:
                fretarray[note.time] += [note.fret]
        except Exception:
            pass
    return fretarray

#%% get dictionary of BPM events and tick numbers
def getBPMDict(chart):
    sync = chart.sync_track
    bpmarray = {}
    for bpm in sync:
        if bpm.kind.value == 'B':
            bpmarray[bpm.time] = bpm.value / 1000
    return bpmarray

def getBPMAtTick(tick, d): #input is a tick number and the result of getBPMDict
    ticklist = d.keys()
    final = 0
    for i in ticklist:
        if tick > i:
            final = d[i]
    return final #in beats per millisecond

def getMSAtTick(tick, d): #input is a tick number and the result of getBPMDict, also fuck this function bc recursion
    ticklist = d.keys()
    #print(ticklist)
    finalbpm = 0
    ticklastbpm = 0
    for i in ticklist:
        if tick <= i:
            break
        ticklastbpm = i
        finalbpm = d.get(i)
        #print(ticklastbpm)
        #print(finalbpm)
    if tick != 0:
        #print(ticklastbpm)
        #print(finalbpm)
        #print(tickstoms(tick - ticklastbpm, finalbpm))
        return tickstoms(tick - ticklastbpm, finalbpm) + getMSAtTick(ticklastbpm, d)
    else:
        return 0

#%%calculate song length, made this before getMSAtTick, probably could've repurposed it but I forgot it existed
def calcsonglength(chart):
    bpmdictionary = getBPMDict(chart)
    fretarray = getFretDict(chart)
    bpmarray = bpmdictionary
    bpmlocs = list(bpmarray.keys())
    songlength = 0
    for k in range(len(bpmlocs) - 1):
        ticklength = bpmlocs[k+1] - bpmlocs[k]
        songlength += tickstoseconds(ticklength, bpmarray[bpmlocs[k]])
    songlength += tickstoseconds(max(fretarray.keys()) - max(bpmlocs), bpmarray[max(bpmlocs)])
    return songlength

#takes offset/noteval dictionary and spits out the note vals in a list
def makeNoteList(fretdict):
    noteList = []
    for tup in fretdict.items():
        noteList += [tup]
    return noteList

#determine if notes should be hopo or not bc on tour assumes every note is strummed and you have to force everything
def naturalHOPOSeq(fretTup):
    firstNote = True
    prevNote = ()
    HOPOSeq = []
    for tup in fretTup:
        if firstNote:
            firstNote = False
            prevNote = tup
            HOPOSeq += [0]
            continue
        if (tup[0] - prevNote[0]) <= 64 and len(tup[1]) == 1 and tup[1][0] != prevNote[1][0]:
            HOPOSeq += [1]
        else:
            HOPOSeq += [0]
        prevNote = tup
    return HOPOSeq


#%%hex bullshit

#yea, no sustains for now
def makeNoteNoSus(offset, color):
    return offset + bytearray(b'\x00\x00') + color

def getNewColor(note):
    color = base
    for val in note:
        if val == 0:
            color += greenHex
        if val == 1:
            color += redHex
        if val == 2:
            color += yellowHex
        if val == 3:
            color += blueHex
    return color

def getColorHex(color):
    return bytearray(color.to_bytes(2, 'little'))

def getOffsetHex(offset):
    return bytearray(offset.to_bytes(4, 'little'))
    

#%% import chart
with open('notes.chart', encoding=('utf-8-sig')) as chartfile:
    chart = chparse.parse.load(chartfile)
xg = chart.instruments[chparse.EXPERT][chparse.GUITAR]
chartlength = len(xg)

fretarray = getFretDict(xg)
bpmarray = getBPMDict(chart)
noteL = makeNoteList(fretarray)
hopoS = naturalHOPOSeq(noteL)

#%%definitions
base = 0x0010
hopo = 0x0040
greenHex = 0x0100
redHex = 0x0200
yellowHex = 0x0400
blueHex = 0x0800


#%% printing diagnostincs
#print(bpmarray)
#print(getMSAtTick(81048, bpmarray))
#print(noteL[500])
#print(hopoS[500])


# turn the tick offsets to ms
newOffsetList = []
for note in noteL:
    newOffsetList += [int(getMSAtTick(note[0], bpmarray))] #this cast may be causing notes close to each other to become chords
#print(newOffsetList)

#%% make the uncompressed qgm, file ext is arbitrary bc what matters is the hex data

with open('chart.qgm', 'wb') as out:
    for counter, offset in enumerate(newOffsetList):
        out.write(getOffsetHex(offset))
        out.write(bytearray(b'\x00\x00'))
        colornum = getNewColor(noteL[counter][1])
        if hopoS[counter]:
            colornum += hopo
        out.write(getColorHex(colornum))
