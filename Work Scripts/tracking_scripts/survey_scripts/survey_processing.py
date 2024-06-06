import pandas as pd
import os
import glob

folder_path = r"C:\Users\beckett.mcfarland\Downloads\Survey Pull"
date_column = 'Approved Date'
site_name_column = 'Site Number'

dtype_dict = {
    8: 'object',
    9: 'object',  # Explicitly setting data type for column 9
    17: 'object',
    18: 'object'
}

# Use glob to find all Excel files
for file in glob.glob(folder_path + "/*.csv"):
    try:
        df = pd.read_csv(file, encoding='utf-8', dtype=dtype_dict, low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(file, encoding='ISO-8859-1', dtype=dtype_dict, low_memory=False)

    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    df = df[pd.notnull(df[date_column])]
    df_sorted = df.sort_values(by=date_column)
    df_sorted[site_name_column] = df_sorted[site_name_column].astype(str).str.extract('(\d+)')

    
    headers_to_keep = [
        "Site Number", "Switch Location", "Type of IDF/Rack", 
        "Number of Switches in IDF/Rack", "Number of Open Ports on Switch", 
        "How many additional switches can this location hold?", 
        "Is conduit full or close to full at this location?", 
        "Does this location utilize a power strip or extension cord instead of a PDU?", 
        "How many open power outlets are available at this location including PDUs?", 
        "Approved Date", "Number of Switches Installed (Including Fiber Switches)", 
        "Number of Switches Not Installed"
    ]

    filtered_df = df_sorted[headers_to_keep]

    # Generating a new filename for the filtered file
    filtered_file_name = os.path.splitext(os.path.basename(file))[0] + '_filtered.csv'
    filtered_df.to_csv(os.path.join(folder_path, filtered_file_name), index=False)
