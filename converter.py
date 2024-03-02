import os
import torchdepth
import os

def deletePics(folder_name):
    try:
        # Get the list of files in the folder
        files = os.listdir(folder_name)
        
        # Iterate over the files and delete them
        for file_name in files:
            file_path = os.path.join(folder_name, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
        
        print("All files deleted successfully.")
    except Exception as e:
        print(f"Error deleting files: {e}")

def convert():
    folder_path = 'images'

    all_files = os.listdir(folder_path)
    png_files = ["images/"+file for file in all_files if file.lower().endswith('.png')]

    deletePics('cloud')
    deletePics('depth')

    for png_file in png_files:
        print(png_file)
        torchdepth.makeDepthAndCloud(png_file)
