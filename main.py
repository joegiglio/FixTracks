import os
from pathlib import Path
import mutagen
from mutagen.flac import FLAC

def singletrack():

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

#singletrack()

def scan_directory(directory_name):
    print("Scanning {}".format(directory_name))

    directory = Path(directory_name)

    for file in os.listdir(directory):
        if file.endswith(".flac"):
            print(file)

            # WORKS
            # flac_file = directory / file
            # print(FLAC(flac_file))
            # print("---")

            flac_file = directory / file
            if FLAC(flac_file["artist"]) == "Unknown artist":
                print("File {} needs to be fixed".format(file))


scan_directory("U:\music\Ripped\EZO\Fire Fire")