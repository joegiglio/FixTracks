import os
from pathlib import Path
import mutagen
from mutagen.flac import FLAC

# U:\music\Ripped\4 Non Blondes
# xdirectory = os.path.join(os.sep, 'u:', os.sep, 'music', os.sep, 'Ripped', os.sep, '4 Non Blondes')
#print(directory)

directory = Path("U:\music\Ripped\EZO\Fire Fire")
bad_filename = "01 Love Junkie.flac" 
bad_file = directory / bad_filename

audio1 = FLAC(bad_file)
print(audio1)

print("---")

good_file = file = directory / "02 Night Crawler.flac"
audio2 = FLAC(good_file)
print(audio2)

print("fixing")

audio1["artist"] = audio2["artist"]
audio1["albumartist"] = audio2["albumartist"]
audio1["album"] = audio2["album"]
audio1["title"] = bad_filename[3:-5]

audio1.pprint()
audio1.save()

# audio["album"] = u"JOE1-album"
# audio["artist"] = u"JOE-artist"
# audio.pprint()
# audio.save()