# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 15:38:44 2020

@author: generalguy26
"""


class song:
    def __init__(self, name, chartoffset, chartlength, audiooffset, audiolength):
        self.name = name
        self.chartoffset = chartoffset
        self.chartlength = chartlength
        self.audiooffset = audiooffset
        self.audiolength = audiolength

adreneline = song('Adrenaline', 0x07028044, 3884, 0x00E11600, 2019328)
allmylife = song('All My Life', 0x07030FE0, 5104, 0x00FFE600, 2643456)
awintb = song('Always Where I Need To Be', 0x0703848C, 2656, 0x01283C00, 1622528)
c2a = song('Call To Arms', 0x07045BE0, 6760, 0x0140FE00, 3080192)
chelsea = song('Chelsea Dagger', 0x0704EB18, 3532, 0x016FFE00, 2155520)
dash = song('Dashboard', 0x07056C44, 4056, 0x0190E200, 2463744)
dimension = song('Dimension', 0x0705DEC4, 1868, 0x01B67A00, 2631168)
dpanic = song('Do The Panic', 0x07064BAC, 2860, 0x01DEA000, 2142208)
egdangerous = song('Everybody Get Dangerous', 0x0706ABD8, 3840, 0x01FF5000, 2064896)
falldown = song('Falling Down', 0x070711EC, 3544, 0x021ED200, 1805312)
htruism = song('Half Truism', 0x07086B88, 4092, 0x023A5E00, 2059776)
iwbym = song('I Wanna Be Your Man', 0x0709CDFC, 4840, 0x0259CC00, 1882624)
lassoo = song('Lassoo', 0x070A5A68, 3056, 0x02768600, 1758208)
lightsandsounds = song('Lights And Sounds', 0x070ABA38, 4880, 0x02915A00, 2086400)
missmurder = song('Miss Murder', 0x070B3D68, 3580, 0x02B13000, 2070016)
paralyzer = song('Paralyzer', 0x070D14D0, 3864, 0x02D0C600, 2105856)
reptilia = song('Reptilia', 0x070DEFB4, 3816, 0x02F0E800, 2191360)
ruby = song('Ruby', 0x070E5884, 2624, 0x03125800, 2130432)
shockwave = song('Shockwave', 0x070F7D28, 6160, 0x0332DA00, 2201600)
stillwaiting = song('Still Waiting', 0x07109AA8, 3820, 0x03547200, 1601536)
sweetsacrifice = song('Sweet Sacrifice', 0x0710F560, 3236, 0x036CE200, 1827840)
tfallen = song('The Fallen', 0x0711D564, 3888, 0x0388C600, 2329088)
tmetal = song('The Metal', 0x071250D0, 4204, 0x03AC5000, 1629184)
taasiaam = song('This Aint A Scene', 0x0712BE18, 3820, 0x03C52C00, 2128384)
unconditional = song('Unconditional', 0x071351D4, 3592, 0x03F39A00, 2008064)
violet = song('Violet Hill', 0x071418BC, 2192, 0x04123E00, 1934848)
whatdihtd = song('What Do I Have To Do', 0x07145EDC, 3200, 0x042FC400, 1880576)
whereawr = song('Where Are We Runnin', 0x07151F74, 2608, 0x044C7600, 1737216)

songlist = [adreneline, allmylife, awintb, c2a, chelsea, dash, dimension, dpanic, egdangerous, falldown, htruism, iwbym, lassoo, lightsandsounds,
            missmurder, paralyzer, reptilia, ruby, shockwave, stillwaiting, sweetsacrifice, tfallen, tmetal, taasiaam, unconditional, violet, whatdihtd, whereawr]

blacklist = []

def choosesong(chartsize, audiosize):
    current = ''
    print(songl.name for songl in blacklist)
    for chart in songlist:
        if chartsize <= chart.chartlength and audiosize <= chart.audiolength and not chart in blacklist:
            if isinstance(current, song):
                if chart.chartlength > current.chartlength or chart.audiolength > current.audiolength or chart in blacklist:
                    continue
            current = chart
    if isinstance(current, song):
        print(current.name)
        print('Chart Offset', hex(current.chartoffset))
        print('Audio Offset', hex(current.audiooffset))
        return current
    else:
        print('Chart or Audio Too Large')
        
    return None
        
def overwriteAudioOffset(rom, audio, replace):
    '''
    Writes the audio data to a rom at the offset of the song to be replaced

            Parameters:
                    rom (file): Modern Hits DS ROM
                    audio (file): song.hwas that you are replacing with
                    replace (song): song in the game files that you are replacing

            Returns:
                    Nothing
    '''
    audioBytes = bytearray(audio)
    endPadding = replace.audiolength - len(audio)
    bytePadString = b'\x00' * endPadding
    audioBytes.extend(bytearray(bytePadString))
    rom.seek(replace.audiooffset)
    rom.write(audioBytes)
    
def overwriteChartOffset(rom, chart, replace):
    '''
    Writes the chart data to a rom at the offset of the song to be replaced

            Parameters:
                    rom (file): Modern Hits DS ROM
                    chart (file): compressed chart.qgm that you are replacing with
                    replace (song): song in the game files that you are replacing

            Returns:
                    Nothing
    '''
    chartBytes = bytearray(chart)
    endPadding = replace.chartlength - len(chart)
    bytePadString = b'\x00' * endPadding
    chartBytes.extend(bytearray(bytePadString))
    rom.seek(replace.chartoffset)
    rom.write(chartBytes)

if __name__ == '__main__':
    rom = open('modernhits.nds', 'rb')
    newrom = open('mhromhack.nds', 'wb+')
    newrom.write(rom.read())
    chart = open('chart.lz77', 'rb').read()
    audio = open('song.hwas', 'rb').read()
    replacing = choosesong(len(chart), len(audio))
    if isinstance(replacing, song):
        while True:
            print('This will replace ', replacing.name, ', is this OK? (Y/N/stop):')
            resp = input()
            if resp == 'Y':
                print('replacing...')
                overwriteAudioOffset(newrom, audio, replacing)
                overwriteChartOffset(newrom, chart, replacing)
                print('done')
                break
            elif resp == 'N':
                blacklist += [replacing]
                replacing = choosesong(len(chart), len(audio))
                print('Next Song...')
            else:
                print('No choice selected, aborting...')

    newrom.close()
