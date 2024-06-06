import shutil
import os

def get_most_recent_file(directory):
    files = os.listdir(directory)
    files = [file for file in files if file.endswith('.xlsx')]  # Filter for Excel files
    if not files:
        print(f"No Excel files found in {directory}")
        return None

    # Get the most recent file based on modification time
    most_recent_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return most_recent_file

if __name__ == "__main__":
    source_directory = r"L:\Rollout\52648 FYE24 Network Refresh Switch\Daily Report"
    destination_directory = r"C:\Users\beckett.mcfarland\Documents\output_excel_files"
    new_filename = "Master Switch Report.xlsx"

    # Get the most recent file in the source directory
    original_filename = get_most_recent_file(source_directory)

    if original_filename:
        source_file = os.path.join(source_directory, original_filename)
        destination_file = os.path.join(destination_directory, new_filename)

        # Copy the file to the destination directory
        shutil.copy(source_file, destination_file)

        print(f"'{original_filename}' has been copied to '{destination_directory}' and renamed '{new_filename}'.")
    else:
        print("No file found to copy.")
