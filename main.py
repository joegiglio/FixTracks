import os
import shutil
import logging
import time
from pathlib import Path
import mutagen
from mutagen.flac import FLAC

DRY_RUN = True  # If True, will not save fixed file.  Use for debugging and testing.
COPY_FIXED_TRACKS = False
COPY_BAD_TRACKS = False

COPY_BAD_TRACKS_DIRECTORY = Path("C:/Users/Joe/Documents/py/FixTracks/FixTracks/bad_tracks")
COPY_FIXED_TRACKS_DIRECTORY = Path("C:/Users/Joe/Documents/py/FixTracks/FixTracks/fixed_tracks")

LOG_FORMAT = "%(levelname)s, %(asctime)s, %(message)s" 

logfile_name = "./log-{}.txt".format(time.time())
logging.basicConfig(filename = Path(logfile_name), level=logging.DEBUG, format=LOG_FORMAT)
logger = logging.getLogger()

# Functions that being with debug_ are not in use.  They were used as building blocks to the final script.

def debug_singletrack():

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

#debug_singletrack()

def debug_scan_directory_old(directory_name):
    # PSUEODO CODE:
    # SCAN THIS DIRECTORY
    # IF FILE, PROCESS AS USUAL
    # IF DIRECTORY, ENTER THAT DIRECTORY AND START THE LOOP AGAIN
    # GETTING TRICKY!

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
                    print(fixed_track_data, directory)
                    flac_file["artist"] = fixed_track_data[0]
                    flac_file["albumartist"] = fixed_track_data[0]
                    flac_file["album"] = fixed_track_data[1]
                    flac_file["title"] = file[3:-5]

                    if COPY_FIXED_TRACKS is True:
                        try:
                            copy_fixed_track(full_path)
                            #flac_file.save()
                        except Exception as e:
                            print("ERROR.  Could not copy fixed track to {} ".format(full_path))    
                            logger.critical("ERROR.  Could not copy fixed track to {} ".format(full_path))
                except Exception as e:
                    print("B")
                    print(fixed_track_data, directory)
                    print("ERROR.  Track 3 may not exist.  Can not fix {} ".format(full_path))    
                    logger.critical("ERROR.  Track 3 may not exist.  Can not fix {} ".format(full_path))
                
            
    if errors_found is False:
        print ("No errors found in directory.")
        logger.info("No errors found in directory.")

   
def debug_process_flac_track(entry, directory):
    #print("found a flac! {}".format(Path(entry)))
    #print(entry)

    errors_found = False

    full_path = entry
    flac_file = FLAC(full_path)
    #print(flac_file["artist"])
            
    if (flac_file["artist"][0]) == "Unknown artist":
        errors_found = True
        print("File {} needs to be fixed".format(entry))
        logger.info("File %s needs to be fixed" % entry)
                
        try:
            fixed_track_data = get_info_from_track_3(directory)
            print(fixed_track_data, directory)
            flac_file["artist"] = fixed_track_data[0]
            flac_file["albumartist"] = fixed_track_data[0]
            flac_file["album"] = fixed_track_data[1]
            flac_file["title"] = entry[3:-5]

            if not DRY_RUN:
                flac_file.save()
                print("File {} fixed".format(entry))
                logger.info("File %s fixed" % entry)
            else:
                print("Dry run.  Logging only.")
                logger.info("Dry run.  Logging only.")

            if COPY_FIXED_TRACKS is True:
                try:
                    copy_fixed_track(full_path)
                except Exception as e:
                    print("ERROR.  Could not copy fixed track to {} ".format(full_path))    
                    logger.critical("ERROR.  Could not copy fixed track to {} ".format(full_path))
        except Exception as e:
            print(directory)
            print("ERROR.  Track 3 may not exist.  Can not fix {} ".format(full_path))    
            logger.critical("ERROR.  Track 3 may not exist.  Can not fix {} ".format(full_path))
          
    if errors_found is False:
        print ("No errors found in directory.")
        logger.info("No errors found in directory.")


def debug_process_directory(entry):
    print("found a directory! {}".format(Path(entry)))


def get_info_from_track_3(directory):
    # I have seen some instances where tracks 1 and 2 are missing data.  I will go to track 3 to retrieve it.
    
    #print("get_info_from_track_3: {}".format(directory))

    track3_found = False

    for file in os.listdir(directory):
        # print(file)
        # print(os.listdir(directory))
                           
        if file.startswith("03 ") and file.endswith(".flac"):
            track3_found = True
            full_path = Path(directory + "/" + file)
            flac_file = FLAC(full_path)
            #print(full_path, flac_file)
            
            artist = flac_file["artist"]
            album = flac_file["album"]
            print("Adding artist:{}, album:{} to track.".format(artist, album))
            logger.info("Adding artist: %s, album: %s to track" % (artist, album))
            return artist, album

        # if not track3_found:        
        #     print("Track 03 not found in {}.  Can not fix file.".format(directory))
        #     logger.fatal("Track 03 not found in {}.  Can not fix file.".format(directory)) 


def copy_fixed_track(full_path):
    print("Copying {} to {}.".format(full_path, COPY_FIXED_TRACKS_DIRECTORY))
    logger.info("Copying %s to %s" % (full_path, COPY_FIXED_TRACKS_DIRECTORY))

    if not os.path.isdir(COPY_FIXED_TRACKS_DIRECTORY):
        os.makedirs(COPY_FIXED_TRACKS_DIRECTORY)
    
    shutil.copy(full_path, COPY_FIXED_TRACKS_DIRECTORY)
    print("File copied.")
    logger.info("File copied.")


def copy_bad_track(full_path):
    print("Copying {} to {}.".format(full_path, COPY_BAD_TRACKS_DIRECTORY))
    logger.info("Copying %s to %s" % (full_path, COPY_BAD_TRACKS_DIRECTORY))

    if not os.path.isdir(COPY_BAD_TRACKS_DIRECTORY):
        os.makedirs(COPY_BAD_TRACKS_DIRECTORY)
    
    shutil.copy(full_path, COPY_BAD_TRACKS_DIRECTORY)
    print("File copied.")
    logger.info("File copied.")


def startup():
    logger.info("=== Script started ===")
    logger.info("Dry run: {}".format(DRY_RUN))

def shutdown():
    logger.info("=== Script ended ===")

def main(path):
    count = 0
    error_count = 0
    print("Processing {}".format(path))
    logging.info("Processing {}".format(path))

    for (root, dirs, files) in os.walk(path):
        #root is the current directory
        #print("Found {} .FLAC files".format(len(files)))
        #print(files)
        
        for file in files:
            if file.endswith(".flac"):
                # print(file)
                # print(root)
                count = count +1

                full_path = Path(root + "/" + "/" + file)
                flac_file = FLAC(full_path)
                #print(flac_file["artist"])
                            
            if (flac_file["artist"][0]) == "Unknown artist":
                errors_found = True
                error_count = error_count + 1
                
                print("==========")
                logger.info("==========")
                
                print("File {} needs to be fixed".format(full_path))
                logger.info("File %s needs to be fixed" % file)

                if COPY_BAD_TRACKS is True:
                    try:
                        copy_bad_track(full_path)
                    except Exception as e:
                        print("ERROR.  Could not copy bad track to {} ".format(full_path))    
                        logger.critical("ERROR.  Could not copy bad track to {} ".format(full_path))

                # Fix track
                try:
                    fixed_track_data = get_info_from_track_3(root)
                    print(fixed_track_data, root)
                    
                    flac_file["artist"] = fixed_track_data[0]
                    flac_file["albumartist"] = fixed_track_data[0]
                    flac_file["album"] = fixed_track_data[1]
                    flac_file["title"] = file[3:-5]
                
                    if not DRY_RUN:
                        flac_file.save()
                        print("File {} fixed".format(full_path))
                        logger.info("File %s fixed" % full_path)
                    else:
                        print("Dry run.  Logging only.")
                        logger.info("Dry run.  Logging only.")
                        #copy_fixed_track(full_path)
                except:
                    print("Unable to find track 03 in {}.  Can not fix track {}.".format(root, full_path))
                    logger.critical("Unable to find track 03 in {}.  Can not fix track {}.".format(root, full_path))
                

    print("Found {} TOTAL .FLAC files. {} errors.".format(count, error_count))

startup()
main("U:\music\Ripped")
shutdown()




