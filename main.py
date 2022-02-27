import os
import shutil
from pathlib import Path
import mutagen
from mutagen.flac import FLAC

COPY_FIXED_TRACKS = True
COPY_BAD_TRACKS = True

COPY_BAD_TRACKS_DIRECTORY = Path("C:/Users/Joe/Documents/py/FixTracks/FixTracks/bad_tracks")
COPY_FIXED_TRACKS_DIRECTORY = Path("C:/Users/Joe/Documents/py/FixTracks/FixTracks/fixed_tracks")

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
            # WORKS
            #print(file)
            # flac_file = directory / file
            # print(FLAC(flac_file))
            # print("---")

            full_path = directory / file
            flac_file = FLAC(full_path)
            #print(flac_file["artist"])
            
            if (flac_file["artist"][0]) == "Unknown artist":
                print("File {} needs to be fixed".format(file))
                flac_file["artist"] = get_info_from_track_3(directory)
                #flac_file["artist"] = "joe-g"
                flac_file.save()

                if COPY_FIXED_TRACKS is True:
                    copy_fixed_track(full_path)


def get_info_from_track_3(directory):
    for file in os.listdir(directory):
        if file.startswith("03 "):
            full_path = directory / file
            flac_file = FLAC(full_path)
            artist = flac_file["artist"]
            print("Adding {} to track.".format(artist))
            return artist


def copy_fixed_track(full_path):
    print("Copying {} to {}.".format(full_path, COPY_FIXED_TRACKS_DIRECTORY))

    if not os.path.isdir(COPY_FIXED_TRACKS_DIRECTORY):
        os.makedirs(COPY_FIXED_TRACKS_DIRECTORY)
    
    shutil.copy(full_path, COPY_FIXED_TRACKS_DIRECTORY)
    print("File copied.")

scan_directory("U:\music\Ripped\EZO\Fire Fire")