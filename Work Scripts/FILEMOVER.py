import os
import shutil

def move_files(source_folder, destination_folder):
    try:
        # Check if source and destination folders exist
        if not os.path.exists(source_folder):
            print(f"Source folder '{source_folder}' does not exist.")
            return

        if not os.path.exists(destination_folder):
            print(f"Destination folder '{destination_folder}' does not exist. Creating it.")
            os.makedirs(destination_folder)

        # Move each file from the source folder to the destination folder
        for item in os.listdir(source_folder):
            source_item = os.path.join(source_folder, item)
            destination_item = os.path.join(destination_folder, item)

            # Check if the item is a file
            if os.path.isfile(source_item):
                shutil.move(source_item, destination_item)
                print(f"Moved '{item}' to '{destination_folder}'.")
            else:
                print(f"Skipping '{item}' as it is not a file.")

        print("All files moved successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Replace with your source and destination folder paths
source_folder = r"L:\Rollout\52642 FYE24 Network Refresh Fiber\Shipping"  # Replace with your source folder path
destination_folder = r"L:\Rollout\52642 FYE24 Network Refresh Fiber\Shipping\Delivered"  # Replace with your destination folder path

move_files(source_folder, destination_folder)
