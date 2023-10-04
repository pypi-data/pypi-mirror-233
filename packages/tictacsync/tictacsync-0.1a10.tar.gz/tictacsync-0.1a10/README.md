# tictacsync

## Warning: this is at pre-alpha stage

Unfinished sloppy code ahead, but should run without errors. Some functionalities are still missing. Don't run the code without parental supervision. Suggestions and enquiries are welcome via the [lists hosted on sourcehut](https://sr.ht/~proflutz/TicTacSync/lists).

## Description

`tictacsync` is a python script to sync audio and video files shot
with [dual system sound](https://www.learnlightandsound.com/blog/2017/2/23/how-to-record-sound-for-video-dual-systemsync-sound)  using a specific hardware timecode generator
called [Tic Tac Sync](https://tictacsync.org). The timecode is named YaLTC for *yet
another longitudinal time code* and should be recorded on a scratch
track on each device for the syncing to be performed, later in _postprod_ before editing.

## Status

`tictacsync`  scans for audio video files and displays their starting time and then merges overlapping audio and video recordings. Multicam syncing with one stereo audio recorder has been tested (spring 2023, [see demo](https://youtu.be/pklTSTi7cqs)). Multi audio recorders coming soon... 


## Installation

This uses the [python interpreter](https://www.python.org/downloads/) and multiple packages (so you need python 3 + pip). Also, you need to install two non-python command line executables: [ffmpeg](https://windowsloop.com/install-ffmpeg-windows-10/) and [sox](https://sourceforge.net/projects/sox/files/). Make sure those are _accessible through your `PATH` system environment variable_.
Then pip install the syncing program:


    pip install tictacsync


This should install python dependencies _and_ the `tictacsync` command.
## Usage

Download some sample files [here](https://tictacsync.org/sampleFiles.zip), unzip and run 

    tictacsync sampleFiles
The resulting synced videos will be in a subfolder named `tictacsynced`. For a very verbose output add the `-v` flag:

    tictacsync -v sampleFiles

When the argument is an unique media file (not a directory), no syncing will occur but the decoded starting time will be printed to stdout:
	
	tictacsync sampleFiles/canon24fps01.MOV

	Recording started at 2023-04-23 01:09:08.1605 UTC
	true sample rate: 48000.545 Hz
	first sync at 37414 samples
	N.B.: all results are precise to the displayed digits!


When called with the `-p` flag, zoomable plots will be produced for diagnostic purpose (close the plotting window for the 2nd one) and the decoded starting time will be output to stdin:

    tictacsync -p sampleFiles/canon24fps01.MOV

Typical first plot produced :

![word](https://mamot.fr/system/media_attachments/files/110/279/794/002/305/269/original/0198908c6eb5c592.png)

Typical second plot produced (note the 34 [FSK](https://en.wikipedia.org/wiki/Frequency-shift_keying) encoded bits `0010111101001111100110000110010000`):
![slicing](https://mamot.fr/system/media_attachments/files/110/279/794/021/372/766/original/6ec62bb417115f52.png)


<!-- To run some tests, from top level `git cloned` dir:

    cd tictacsync ; python -m pytest
 Yes, the coverage is low. -->