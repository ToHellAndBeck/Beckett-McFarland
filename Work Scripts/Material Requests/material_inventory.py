import os
import pandas as pd
from openpyxl import load_workbook
import re

# Configuration
source_directory = r'L:\Rollout\97820 WM - Switch-Fiber FYE25 Network Refresh - CJE\Shipping\Current'  # Typo in directory name, please verify
target_excel_file = r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Material Requests\Output\inventory_script_output.xlsx"
cell_range = 'D16:G32'  # Update this to the range of cells you want to extract text from

# Define your headers and associated keywords
header_keywords = {
    "CISCO ENCS 5412 12-CORE INTEl 16G DRA": ["NHOST01"],
    "EX4600-Ethernet Switch": ["UPC1","UPC2"],
    "QFX-QSFP-DAC-3M": ["40 GIG"],
    "EX2300-48 port Ethernet Switch": ["LP2","SPARE SWITCH"],
    "Juniper Wall Mount Kit": [],
    "PRE-SFP10G-SR-JNPR": ["10"],
    "PRE-SFP-10-JNPR (1G LX)": ["1 GIG"],
    "EX_10G Direct Attached Copper (DAC 1M)": ["STACKING CABLES"],
    "Paging Adapter and Scheduler": ["ALGO"],
    "PRE-SFP10G-T-JNPR (COPPER)": ["RJ45"]
}

headers = list(header_keywords.keys())
date_pattern = r'\d{1,2}-\d{1,2}-\d{2}'

# Function to extract all text from the specified cell range
def extract_text(sheet, cell_range):
    extracted_items = []
    for row in sheet[cell_range]:
        for cell in row:
            if cell.value:
                extracted_items.append(str(cell.value).strip())
    return '; '.join(extracted_items)

# Function to map cell content to header
def map_to_header(cell_content):
    for header, keywords in header_keywords.items():
        if any(keyword in cell_content for keyword in keywords):
            return header
    return None

# Initialize a DataFrame
df = pd.DataFrame(columns=['Filename', 'Date', 'All Extracted Text'] + headers)
extracted_rows = []

for filename in os.listdir(source_directory):
    if filename.endswith('.xlsx'):
        date_match = re.search(date_pattern, filename)
        date_in_filename = date_match.group(0) if date_match else 'Unknown Date'
        file_path = os.path.join(source_directory, filename)
        workbook = load_workbook(filename=file_path, read_only=True)
        sheet = workbook.active

        # Extract all text from the specified range
        all_text = extract_text(sheet, cell_range)

        # Initialize a row with empty strings for each header
        row = {header: '' for header in headers}

        # Extract text from the specified range and map to headers
        for row_cells in sheet[cell_range]:
            for cell in row_cells:
                if cell.value:
                    header = map_to_header(str(cell.value))
                    if header:
                        # Append cell value under the appropriate header
                        row[header] += str(cell.value) + '; '

        # Append the dict to the extracted_rows list
        extracted_rows.append({
            'Filename': filename,
            'Date': date_in_filename,
            'All Extracted Text': all_text,  # Adding the all_text extracted
            **{k: v.rstrip('; ') for k, v in row.items()}
        })

        # Close the workbook
        workbook.close()

# After collecting all rows, create the DataFrame
df = pd.DataFrame(extracted_rows, columns=['Filename', 'Date', 'All Extracted Text'] + headers)

# Save the DataFrame to a new Excel file
df.to_excel(target_excel_file, index=False)

print(f'Extraction and saving completed successfully. Output can be found at {target_excel_file}')
