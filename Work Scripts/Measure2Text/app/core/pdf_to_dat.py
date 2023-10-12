from . import constants
import os
from pypdf import PageObject, PdfReader
import re


def get_new_pdfs():
    return [
        os.path.join(constants.NEW_PDF_DIR, pdf_name)
        for pdf_name in os.listdir(constants.NEW_PDF_DIR)
    ]

def load_pdf(pdf_path:str):
    return PdfReader(pdf_path)

def dimenstion_str_to_float(text: str):
    # Remove unwanted characters and strip leading/trailing spaces
    cleaned_text = text.replace("ft", "").replace("*", "").replace("'", "").strip()

    # Check if the cleaned text is empty
    if not cleaned_text:
        return None  # Return None for empty text

    # Convert to float
    return float(cleaned_text)
def get_page_text(page:PageObject):
    return page.extract_text().splitlines()

def is_dimension_location_line(line:str):
    return "dimension" in line.lower()

def get_dimension_location_from_line(line:str):
    for name in constants.PDF_LOCATION_KEYS:
        if name in line.lower():
            return name

def convert_dimension_text_2_object(line: str):
    data = {}
    
    dimensions_in_line = re.findall(r'\d+', line)
    print(dimensions_in_line)
    
    # If there are multiple dimensions (a list of values)
    if len(dimensions_in_line) > 1:
        for idx, dimension_text in enumerate(dimensions_in_line):
            # Handle the case where idx exceeds the length of DIMENSION_KEYS
            if idx < len(constants.DIMENSION_KEYS):
                dimension_value = dimenstion_str_to_float(dimension_text)
                dimension = constants.DIMENSION_KEYS[idx]
                data[dimension] = dimension_value
    # If there's a single dimension (a string)
    elif len(dimensions_in_line) == 1:
        # Handle the case where idx exceeds the length of DIMENSION_KEYS
        idx = 0  # Assuming there's only one dimension
        if idx < len(constants.DIMENSION_KEYS):
            dimension_value = dimenstion_str_to_float(dimensions_in_line[0])
            dimension = constants.DIMENSION_KEYS[idx]
            data[dimension] = dimension_value

    return data

def format_dimension_float_as_dat(dimension_data:dict[str, float]):
    length = dimension_data.get("length")
    width = dimension_data.get("width")
    return "\n".join([
        f"{constants.DAT_FORMAT_PREFIX_1}{length}{constants.DAT_LENGHT_FORMAT}",
        f"{constants.DAT_FORMAT_PREFIX_1}{width}{constants.DAT_WIDTH_FORMAT}",
        f"{constants.DAT_FORMAT_PREFIX_2}{length}{constants.DAT_LENGHT_FORMAT}",
        f"{constants.DAT_FORMAT_PREFIX_2}{width}{constants.DAT_WIDTH_FORMAT}"
    ])

def create_dat_file_text(location: str, formatted_data: str):
    file_text_list = []
    if location:
        file_text_list.append(constants.DAT_LOCATION_TEXT + location.title().strip())
    else:
        # Handle the case where location is None
        file_text_list.append(constants.DAT_LOCATION_TEXT + "Unknown Location")

    file_text_list.append(constants.DAT_PREFIX)
    file_text_list.append(formatted_data)
    file_text_list.append(constants.DAT_POSTFIX)
    return "\n".join(file_text_list)


def save_text_to_dat_file_and_return_path(location: str, formatted_text: str):
    if location:
        file_name = location + '.dat'
    else:
        file_name = 'unknown_location.dat'

    file_path = os.path.join(constants.OUTPUT_DIR, file_name)
    with open(file_path, 'w') as fp:
        fp.write(formatted_text)
    return file_path

def move_pdf(pdf_path):
    pdf_name = os.path.basename(pdf_path)
    move_to_path = os.path.join(constants.OLD_PDF_DIR, pdf_name)
    try:
        os.rename(pdf_path, move_to_path)
        return True
    except:
        return False
    