from datetime import datetime as dt
from os.path import abspath, basename, join
from os.path import exists

import pandas as pd

from openpyxl import load_workbook

SCRIPT_PATH = r"C:\Users\beckett.mcfarland\Documents\output_excel_files"
SCRIPT_DIR = SCRIPT_PATH.replace(basename(SCRIPT_PATH), "")
TODAY = dt.now()

# destination settings
F_NAME_DATE_FORMAT = "%m-%d-%y"
TODAY_STR = dt.strftime(TODAY, F_NAME_DATE_FORMAT)
DST_F_PREFIX = f"Switch Report {TODAY_STR} - Python"
DST_F_POSTFIX = ".xlsx"
DST_F_NAME = DST_F_PREFIX + DST_F_POSTFIX
DST_DIR = SCRIPT_DIR
DST_F_PATH = join(DST_DIR, DST_F_NAME)
DST_SHEET_NAME = "DAILY DUMP"
# source  settings
F_NAME_REQUIREMENTS = [
    "Master",
    "Switch",
    "Report",
]  # accept only files that contain these
F_TYPES_ALLOWED = [".xlsx", ".xlsm"]  # accept only files that end in these
SRC_F_DIR = r'L:\Rollout\52648 FYE24 Network Refresh Switch\Daily Report'  # change this to the directory the source file is located
SRC_SHEET_NAME = "Conference Call Switch"
MIN_SRC_COLUMNS = 5

def file_meets_requirements(f_name: str):
    for ending in F_TYPES_ALLOWED:
        if f_name.endswith(ending):
            for requirement in F_NAME_REQUIREMENTS:
                if requirement not in f_name:
                    return False
            return True

def get_most_recent_file(f_dir: str):
    most_recent_name = None
    most_recent_time = None
    for f_name in listdir(f_dir):
        if file_meets_requirements(f_name):
            f_path = join(f_dir, f_name)
            f_time = getmtime(f_path)
            if not most_recent_name:
                most_recent_name = f_name
                most_recent_time = f_time
            else:
                if f_time > most_recent_time:
                    most_recent_name = f_name
                    most_recent_time = f_time

    if most_recent_name is not None:
        return join(f_dir, most_recent_name)
    else:
        print("No file found that meets the requirements.")
        return None  # Return a meaningful value when no file is found

file_to_wrk = get_most_recent_file(SRC_F_DIR)
src_wb = load_workbook(file_to_wrk, data_only=True)

if not exists(DST_F_PATH):
    dst_wb = src_wb  # Use the source workbook as the destination workbook
    dst_wb.save(DST_F_PATH)
    dst_wb.close()

with pd.ExcelWriter(DST_F_PATH, mode="a", if_sheet_exists="overlay") as writer:
    src_wb[SRC_SHEET_NAME].to_excel(writer, sheet_name=DST_SHEET_NAME)

print(f"The sheet '{SRC_SHEET_NAME}' has been appended to '{DST_F_NAME}'.")
