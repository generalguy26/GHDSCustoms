# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:44:09 2019
@author: generalguy26
"""

import chparse

def tickstoseconds(ticks, bpm):
    return ticks / 192 * 60 / bpm  #192 ticks per beat divided by beats per second
                                    #this is hardcoded to the resolution, may need to pull from metadata of the song
                                    #currently, just make sure your charts are 4fret and resolution is set to 192
def tickstoms(ticks, bpm):
    return ticks / 192 * 60 / bpm * 1000

#%%Other Detection
        
def printchart(notes): #unused function to print the chart to the terminal, used in old project
    for note in (notes[::-1]):
        notestring = '- - - - -'
        lns = list(notestring)
        for fret in note:
            lns[2 * fret] = 'O'
        print(''.join(lns))
        
#%% add notes to a dictionary cooresponding to their tick number, and group chords together
def getFretDict(chart):                                              #load chparse xguitar chart, function is repurposed from previous project
    fretarray = {}                                                   #initialize empty dictionary, will contain tick offset and note value
    for note in xg:
        try:
            if fretarray.get(note.time, -1) == -1:                   #creates new dictionary entry if none exists for the offset of the note
                fretarray[note.time] = [[note.fret], note.length]
            else:                                                    #adds fret value to offset entry if osset value exists; this is how chords are made
                fretarray[note.time][0] += [note.fret]
        except Exception:                                            #this fixes events that aren't notes and therefore don't have fret values (e.g. anchors)
            pass
    return fretarray

#%% get dictionary of BPM events and tick numbers
def getBPMDict(chart):                                               #load bpm from chparse chart directly, function is repurposed from previous project
    sync = chart.sync_track                                          #get sync track from chart, this is different than getFretDict where this is basically the argument, don't remember why it's different
    bpmarray = {}                                                    #initialize empty dictionary of bpm offsets and values
    for bpm in sync:
        if bpm.kind.value == 'B':                                    #pull out bpm events from sync_track
            bpmarray[bpm.time] = bpm.value / 1000                    #sync_track bpm is in ms, so convert to bpm (this may be causing slight inaccuracies with decimal bpms)
    return bpmarray

def getBPMAtTick(tick, d):                                           #input is a tick number and the result of getBPMDict, returns the bpm value at the specified tick
    ticklist = d.keys()                                              #list of bpm offsets
    final = 0                                                        #initialization
    for i in ticklist:                                               #iterate through bpm offsets and find the bpm entry that's before the tick argument
        if tick > i:                                                 #is the tick argument after the bpm's tick location
            final = d[i]                                             #sets return value to bpm value at the offset
    return final                                                     #in beats per millisecond

def getMSAtTick(tick, d):                                            #input is a tick number and the result of getBPMDict, also fuck this function bc recursion
    ticklist = d.keys()                                              #list of bpm offsets
    #print(ticklist) #diagnostic
    finalbpm = 0                                                     #initialization
    ticklastbpm = 0                                                  #initialization
    for i in ticklist:                                               #this is basically getBPMAtTick but rewritten slightly
        if tick <= i:
            break
        ticklastbpm = i                                              #get tick value of the last bpm event
        finalbpm = d.get(i)                                          #get bpm value at that tick
        #print(ticklastbpm)
        #print(finalbpm)
    if tick != 0:                                                    #needed to not fuck up the recursion
        #print(ticklastbpm)
        #print(finalbpm)
        #print(tickstoms(tick - ticklastbpm, finalbpm))
        return tickstoms(tick - ticklastbpm, finalbpm) + getMSAtTick(ticklastbpm, d) #this recursion calculates the ms length of every bpm section and adds them together
    else:                                                                            #base case for recursion
        return 0

#%%calculate song length, made this before getMSAtTick, probably could've repurposed it but I forgot it existed
def calcsonglength(chart):                                            #function is deprecated and unused
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


def makeNoteList(fretdict):                                             #takes offset/noteval dictionary and spits out the note vals in a list
    noteList = [] #
    for tup in fretdict.items():                                        #converts dictionary to list with entries of the dictionary items in form of (offset, [[fret values], sus length])
        noteList += [tup]                                               #includes the sustain length 
    return noteList


def naturalHOPOSeq(fretTup):                                            #determine if notes should be hopo or not bc on tour assumes every note is strummed and you have to force everything 
    firstNote = True
    prevNote = ()
    HOPOSeq = []                                                        #initialization, will be list of flags cooresponding to hopo flags
    for tup in fretTup:
        if firstNote:
            firstNote = False
            prevNote = tup                                              #first note is always a strum
            HOPOSeq += [0]
            continue
        if (tup[0] - prevNote[0]) <= 64 and len(tup[1][0]) == 1 and tup[1][0] != prevNote[1][0]: #if current note is less than or equal to 64 ticks from the previous note, mark cooresponding flag as hopo
            HOPOSeq += [1]
        else:
            HOPOSeq += [0]
        prevNote = tup                                                  #setting previous note to current note for reference in next iteration
    return HOPOSeq


#%%hex bullshit

#sustains have been implemented, so this is deprecated
def makeNoteNoSus(offset, color):
    return offset + bytearray(b'\x00\x00') + color

def getNewColor(note):                                                  #turns note value list into hex value for ghds
    color = base                                                        #all notes start with 0x10, then add values depending on gems, note info, etc
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

def getColorHex(color):                                                 #conversion of note info to little endian
    return bytearray(color.to_bytes(2, 'little'))

def getOffsetHex(offset):                                               #conversion of ms offset to little endian
    return bytearray(offset.to_bytes(4, 'little'))

def forceHOPOs(hopoS, hopoF):                                           # not implemented bc I haven't bothered with getting force info from chparse
    return [not hopoS[index] if hopoF[index] else hopoS[index] for index, val in enumerate(hopoS)] # this is stupid but I think it works

    

#%% import chart
with open('notes.chart', encoding=('utf-8-sig')) as chartfile:          # breaks without the encoding, loads the chart file
    chart = chparse.parse.load(chartfile)                               # creating chparse chart object
xg = chart.instruments[chparse.EXPERT][chparse.GUITAR]                  # getting expertguitar info
chartlength = len(xg)

fretarray = getFretDict(xg)                                             # create dictionary of tick offsets with note values
bpmarray = getBPMDict(chart)                                            # create dictionary of tick offsets with bpm values
noteL = makeNoteList(fretarray)                                         # create list of tick offsets with bpm values
hopoS = naturalHOPOSeq(noteL)                                           # create list of hopo flags

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
# print(fretarray)
# print(noteL)
# print(hopoS)

# turn the tick offsets to ms
newOffsetList = []
for note in noteL:
    newOffsetList += [int(getMSAtTick(note[0], bpmarray))]                # creates list of ms offsets
#print(newOffsetList)
#%% make the uncompressed qgm, file ext is arbitrary bc what matters is the hex data

with open('chart.qgm', 'wb') as out:                                      # finally writing the qgm file, writing 8 bytes for each note; 4 bytes offset, 2 bytes sustain length, 2 bytes note info
    for counter, offset in enumerate(newOffsetList):                      # enumerate to keep track of what note we're at in noteL
        out.write(getOffsetHex(offset))                                   # write 4 bytes of the ms offset
        
        #implementation of sustains
        offsetBPM = getBPMAtTick(noteL[counter][0], bpmarray)             # get bpm at current note tick offset
        suslengthTick = noteL[counter][1][1]                              # get sustain length in ticks
        suslengthMS = int(tickstoms(suslengthTick, offsetBPM))            # lazy convert not using recursion of ticks to ms, def what is causing weird extended sustains
        out.write(bytearray(suslengthMS.to_bytes(2, 'little')))           # write 2 bytes sustain length data
        
        colornum = getNewColor(noteL[counter][1][0])                      # get color hex value of current note
        if hopoS[counter]:                                                # is the current note hopo flag set to 1?
            colornum += hopo                                              # add hopo value
        out.write(getColorHex(colornum))                                  # write 2 bytes note info
