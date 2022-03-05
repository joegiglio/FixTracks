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

def scan_directory_old(directory_name):
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
                    print("A")
                    fixed_track_data = get_info_from_track_3(directory)
                    print(fixed_track_data, directory)
                    flac_file["artist"] = fixed_track_data[0]
                    flac_file["albumartist"] = fixed_track_data[0]
                    flac_file["album"] = fixed_track_data[1]
                    flac_file["title"] = file[3:-5]

                    if COPY_FIXED_TRACKS is True:
                        try:
                            copy_fixed_track(full_path)
                            flac_file.save()
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

def scan_directory(directory_name):
    # PSUEODO CODE:
    # SCAN THIS DIRECTORY
    # IF FILE, PROCESS AS USUAL
    # IF DIRECTORY, ENTER THAT DIRECTORY AND START THE LOOP AGAIN
    # GETTING TRICKY!

    print("Scanning {}".format(directory_name))
    logger.info("Scanning %s" % directory_name)

    directory = Path(directory_name)

    for entry in os.scandir(directory):
        if entry.is_file():
            if entry.name.endswith(".flac"):
                process_flac_track(Path(entry), directory)
               
        elif entry.is_dir():
            process_directory(Path(entry))
        
    
def process_flac_track(entry, directory):
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

            if COPY_FIXED_TRACKS is True:
                try:
                    copy_fixed_track(full_path)
                    flac_file.save()
                except Exception as e:
                    print("ERROR.  Could not copy fixed track to {} ".format(full_path))    
                    logger.critical("ERROR.  Could not copy fixed track to {} ".format(full_path))
        except Exception as e:
            print(directory)
            print("xERROR.  Track 3 may not exist.  Can not fix {} ".format(full_path))    
            logger.critical("ERROR.  Track 3 may not exist.  Can not fix {} ".format(full_path))
          
    if errors_found is False:
        print ("No errors found in directory.")
        logger.info("No errors found in directory.")


def process_directory(entry):
    print("found a directory! {}".format(Path(entry)))


def get_info_from_track_3(directory):
    # I have seen some instances where tracks 1 and 2 are missing data.  I will go to track 3 to retrieve it.
    print("AAAAA")
    print(directory)

    counter = 0
    for file in os.listdir(directory):
        counter += 1
        print(counter)
        print(file)
        print(os.listdir(directory))
                           
        if file.startswith("03 "):
            full_path = directory / file
            flac_file = FLAC(full_path)
            print("debug!")
            print(full_path, flac_file)
            artist = flac_file["artist"]
            album = flac_file["album"]
            print("Adding artist:{}, album:{} to track.".format(artist, album))
            logger.info("Adding artist: %s, album: %s to track" % (artist, album))
            return artist, album
        else:
            print("debug - not 03")
        
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


def copy_bad_track(full_path):
    print("Copying {} to {}.".format(full_path, COPY_BAD_TRACKS_DIRECTORY))
    logger.info("Copying %s to %s" % (full_path, COPY_BAD_TRACKS_DIRECTORY))

    if not os.path.isdir(COPY_BAD_TRACKS_DIRECTORY):
        os.makedirs(COPY_BAD_TRACKS_DIRECTORY)
    
    shutil.copy(full_path, COPY_BAD_TRACKS_DIRECTORY)
    print("File copied.")
    logger.info("File copied.")


def finalize():
    logger.info("=== Script ended ===")

def directory_dump(path):
    print (path)

    for entry in os.scandir(path):
        if entry.is_dir():
            print("{} is dir".format(Path(entry)))
            scan_directory(Path(entry))
        elif entry.is_file():
            print("{} is file".format(Path(entry)))


def dir_test(path):
    print (path)

    for file in os.listdir(path):
        #print(file)
        if file.startswith("W"):
            print(file)


def walk_test(path):
    count = 0
    error_count = 0
    print (path)

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
                print("File {} needs to be fixed".format(full_path))
                logger.info("File %s needs to be fixed" % file)

                if COPY_BAD_TRACKS is True:
                    try:
                        copy_bad_track(full_path)
                    except Exception as e:
                        print("ERROR.  Could not copy bad track to {} ".format(full_path))    
                        logger.critical("ERROR.  Could not copy bad track to {} ".format(full_path))

    print("Found {} TOTAL .FLAC files. {} errors.".format(count, error_count))


#directory_dump(Path("U:\music\Ripped"))
#scan_directory("U:\music\Ripped\EZO\Fire Fire")
#scan_directory("U:\music\Ripped")
#dir_test("U:\music\Ripped")
walk_test("U:\music\Ripped")

finalize()




