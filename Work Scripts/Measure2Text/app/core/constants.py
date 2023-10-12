import os

#directory structure
CONSTANTS_PATH = os.path.abspath(__file__)
CORE_DIR = CONSTANTS_PATH.replace(os.path.basename(CONSTANTS_PATH), "")
print(CORE_DIR)
if CORE_DIR.endswith(os.path.sep):
    CORE_DIR = CORE_DIR[:-2]
PATH_LIST = CORE_DIR.split(os.sep)
PATH_LIST[-1] = "output"
OUTPUT_DIR = os.sep.join(PATH_LIST)
print(OUTPUT_DIR)
PATH_LIST[-1] = "pdfs"
PATH_LIST.append("new")
NEW_PDF_DIR = os.sep.join(PATH_LIST)
print(r"C:\Users\beckett.mcfarland\Desktop\pdf2dat\app\pdfs\new")
print(NEW_PDF_DIR)
PATH_LIST[-1] = "old"
OLD_PDF_DIR = os.sep.join(PATH_LIST)
#dat file formatting
DAT_LOCATION_TEXT = "name="
DAT_PREFIX = """
height=2.4
thickness=0.18
inverse=False
ceiling=False
floor=False
close=False
#
# Walls
#
walls=4
"""
DAT_POSTFIX = """
#
# Baseboard
#
baseboard=True
baseh=0.12
baset=0.015
#
# Wall Cover
#
shell=False
shellh=0.2
shellt=0.025
shellf=1.0
shellb=1.0
#
# Materials
#
materials=True
"""
PDF_LOCATION_KEYS = ['outside','1st floor', 'sales floor', 'office 1', 'office 2', 'office 3', 'warehouse', 'racks']
PATTERN = PATTERN = [r'\b\w+ft\b', r'(\d+)\s*x\s*(\d+)',r'(\d+\'?)\s*x\s*(\d+\'?)',r'(\d+(\.\d+)?)\s*ft\s*x\s*(\d+(\.\d+)?)\s*ft',r'(\d+(\.\d+)?)\s*ft',r'(\d+)\*(\d+)',r'(\d+)(\*\d+)*',r'\d+']
DIMENSION_KEYS = ["length", "width","height"]
DAT_FORMAT_PREFIX_1 = "w="
DAT_FORMAT_PREFIX_2 = "w=-"
DAT_LENGHT_FORMAT = ",a=False,r=0.0,h=0,m=0.0,f=0.0,c=False,cf=1.0,cd=180.0,cs=12"
DAT_WIDTH_FORMAT = ",a=False,r=90.0,h=0,m=0.0,f=0.0,c=False,cf=1.0,cd=180.0,cs=12"
