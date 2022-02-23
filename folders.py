import os

directory = input("What is the directory? ")
print(directory)

directory_exists = os.path.exists(directory)
#print(directory_exists)

if not directory_exists:
    print("Directory does not exist.")
else:
    while True:
        try:
            file_type = int(input("Choose file type:\n 1. FLAC\n 2. MP3\n"))
            
            if file_type <1 or file_type >2:
                print("Invalid choice.")
            else:
                print("Valid choice.")
        except ValueError:
            print("Not an integer.")
