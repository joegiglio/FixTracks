import os
import shutil
import logging
from pathlib import Path
import mutagen
from mutagen.flac import FLAC

COPY_FIXED_TRACKS = True
COPY_BAD_TRACKS = True

COPY_BAD_TRACKS_DIRECTORY = Path("C:/Users/Joe/Documents/py/FixTracks/FixTracks/bad_tracks")
COPY_FIXED_TRACKS_DIRECTORY = Path("C:/Users/Joe/Documents/py/FixTracks/FixTracks/fixed_tracks")

LOG_FORMAT = "%(levelname)s, %(asctime)s, %(message)s" 

logging.basicConfig(filename = Path("./logging.txt"), level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()

logger.info("=== Script started ===")

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

    #audio1.pprint()
    #audio1.save()

#singletrack()

def scan_directory(directory_name):
    print("Scanning {}".format(directory_name))
    logger.info("Scanning %s" % directory_name)

    directory = Path(directory_name)

    errors_found = False

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
                errors_found = True
                print("File {} needs to be fixed".format(file))
                logger.info("File %s needs to be fixed" % file)
                
                try:
                    fixed_track_data = get_info_from_track_3(directory)
                    flac_file["artist"] = fixed_track_data[0]
                    flac_file["albumartist"] = fixed_track_data[0]
                    flac_file["album"] = fixed_track_data[1]
                    flac_file["title"] = file[3:-5]

                    if COPY_FIXED_TRACKS is True:
                        copy_fixed_track(full_path)
                        #### flac_file.save()
                except Exception as e:
                    print("ERROR.  Track 3 may not exist.  Can not fix {} ".format(full_path))    
                    logger.critical("ERROR.  Track 3 may not exist.  Can not fix {} ".format(full_path))
                
            
    if errors_found is False:
        print ("No errors found in directory.")
        logger.info("No errors found in directory.")


def get_info_from_track_3(directory):
    # I have seen some instances where tracks 1 and 2 are missing data.  I will go to track 3 to retrieve it.

    for file in os.listdir(directory):
        
        if file.startswith("03 "):
            full_path = directory / file
            flac_file = FLAC(full_path)
            artist = flac_file["artist"]
            album = flac_file["album"]
            print("Adding artist:{}, album:{} to track.".format(artist, album))
            logger.info("Adding artist: %s, album: %s to track" % (artist, album))
            return artist, album
        
        print("Track 03 not found.  Can not fix {}.".format(flac_file))
        logger.fatal("Track 03 not found.  Can not fix {}.".format(flac_file)) 


def copy_fixed_track(full_path):
    print("Copying {} to {}.".format(full_path, COPY_FIXED_TRACKS_DIRECTORY))
    logger.info("Copying %s to %s" % (full_path, COPY_FIXED_TRACKS_DIRECTORY))

    if not os.path.isdir(COPY_FIXED_TRACKS_DIRECTORY):
        os.makedirs(COPY_FIXED_TRACKS_DIRECTORY)
    
    shutil.copy(full_path, COPY_FIXED_TRACKS_DIRECTORY)
    print("File copied.")
    logger.info("File copied.")

def finalize():
    logger.info("=== Script ended ===")

#scan_directory("U:\music\Ripped\EZO\Fire Fire")
#finalize()

def directory_dump(path):
    print (path)

    for entry in os.scandir(path):
        if entry.is_dir():
            print("{} is dir".format(Path(entry)))
            scan_directory(Path(entry))
        elif entry.is_file():
            print("{} is file".format(Path(entry)))

directory_dump(Path("U:\music\Ripped"))


