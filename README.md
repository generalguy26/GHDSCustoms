# GHDSCustoms

UPDATE 4/10/23:
This is a set of files used in the creation of custom songs for Guitar Hero DS. To quickly import a prepared song, put all of the files here in the same folder as `notes.chart`, `song.wav`, and `modernhits.nds`. Python must be installed and added to the system PATH, and the python packages [chparse](https://github.com/Kenny2github/chparse) and [ndspy](https://github.com/RoadrunnerWMC/ndspy) must also be installed. Run convert.py to convert a chart to qgm format, then run chartcompression.py to compress it with the lz77 algorithm. Then, create the audio track by dragging a 19996 Hz mono 16 bit sample wav onto the IMAADPCMEncoder, then run insertsong.py to inject the custom song into the game.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
old description:
This is a set of files used in the creation of custom songs for Guitar Hero DS. To quickly import a prepared song, put all of the files here in the same folder as `notes.chart`, `song.wav`, and `modernhits.nds`. Python and Sox Sound Exchange must be installed and added to the system PATH, and the python packages [chparse](https://github.com/Kenny2github/chparse) and [ndspy](https://github.com/RoadrunnerWMC/ndspy) must also be installed. Running `run.bat` will execute the files in the correct order, and among other files, will generate a modified `mhromhack.nds` file.
