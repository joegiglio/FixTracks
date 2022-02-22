import os
from pathlib import Path
import mutagen
from mutagen.flac import FLAC

# U:\music\Ripped\4 Non Blondes
# xdirectory = os.path.join(os.sep, 'u:', os.sep, 'music', os.sep, 'Ripped', os.sep, '4 Non Blondes')
#print(directory)

directory = Path("U:/music/Ripped/4 Non Blondes/Bigger, Better, Faster, More!")
#file = directory / "01 Train.flac"
file = directory / "06 spaceman.flac"

#f = open(file)
# print(f.read())

audio = FLAC(file)
print(audio)