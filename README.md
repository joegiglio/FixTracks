# FixTracks
Fix missing metadata from FLAC files ripped by Windows Media Player

Due to a long running bug in Windows Media Player (https://social.technet.microsoft.com/Forums/en-US/373931c5-1a94-4fd7-9b83-8549fc27038a/first-track-of-ripped-cds-in-wav-format-does-not-display-track-info-in-windows-explorer?forum=w7itpromedia), many people have complained about ripping their CD library only to later realize that some of the tracks (usually the first of an album) do not have Artist and Album data.  This makes services such as Youtube Music stick these "stray songs" in the Unknown Artist folder after you upload them. 

The workaround is to not let Windows Media Player auto rip CDs.  You need to insert the CD and wait a few seconds before clicking the Rip button.  This usually fixes it but will slow you down if you have lots of CDs to rip through.

But what to do about that library of albums that have incorrect data?  This project fixes it... at least for FLAC files.  I understand MP3, and perhaps other formats, have the same problem.

**Requirements**

This script was written with Python 3.10.2.  It uses the Mutagen package which can be installed following the steps below.  

**Instructions**

1. Clone project
2. Create virtual environment and switch to it. (https://docs.python.org/3/library/venv.html)
3. Run "pip install -r requirements.txt" which will install the Mutagen package.
4. Open the main.py file and set values for the constants up top:

TRACKS_LOCATIONS is the directory where your music is saved.  The root of your music directory is fine since this script will traverse the entire directory tree. 

_DRY_RUN_ - Set to True if you want to create a logfile and not actually change the files yet.  Recommended best practice is to set this to True so you can watch the output and log file without changing any of your files yet.  Once you are satisfied with the changes the script will make, set this to False and run it again.    

_COPY_FIXED_TRACKS_ - If set to True will copy the fixed Flac files to the designated directory. 

_COPY_FIXED_TRACKS_DIRECTORY_ - Used in conjunction with the COPY_FIXED_TRACKS setting.

_COPY_BAD_TRACKS_ - If set to True will copy the bad Flac files to the designated directory.  Use this as a backup copy, just in case...

_COPY_BAD_TRACKS_DIRECTORY_ - Used in conjunction with the COPY_BAD_TRACKS setting.

5.  Run the script using "python main.py".  If you don't see much output to the screen, let it run... it can take several minutes to traverse large directory trees especially on external drives. 
6.  The script will output to the screen and a "log-".txt file will be created.  Every time you run the script, a new log file will be generated. 
7.  Closely review the log file for anything odd.  The script is written to pull the file metadata file from the third track in a directory which should be safe.  However, I did have one example where the FIRST FIVE tracks did not have the metadata.  Manually fixing file 3 and running the script again fixed the rest of the files.
8.  Once you are satisfied with the cleanup, you can re-upload the albums to a service such as Youtube Music.  I have come to learn that uploading just the file will stick the tracks at the END of the album.  This is usually not what you want since the first track is usually the broken one.  To avoid this, try re-uploading the ENTIRE album.  This is what worked for me!  If that STILL doesn't work, try deleting the album from Youtube Music and then re-uploading it.  

SPECIAL NOTE: Albums from Various Artists might not have the song artist, even after the running this script.  Some CDs just don't seem to have that data.

I built this script over time and left most of the test code behind for posterity.  If you are interested in learning from the code, open the main.py file and scroll to the bottom.  The script calls the "startup" and then "main" functions.

**Future Features**

1.  Support for other file types
2.  Add a GUI for less technical users

Please feel free to contribute code to this project.  

