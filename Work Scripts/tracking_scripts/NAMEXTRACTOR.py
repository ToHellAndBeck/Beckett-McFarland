import os
import fitz  # PyMuPDF
import openpyxl
import re

# Directory containing PDF files
pdf_directory = r"C:\Users\beckett.mcfarland\Documents\PDFs"  # Replace with the actual directory path

# Initialize lists to store extracted names and tracking numbers
all_names = []
all_tracking_numbers = []

# Regular expression pattern for uppercase words
uppercase_word_pattern = r'\b[A-Z]+\b'

# Iterate through each PDF file in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('.pdf'):
        pdf_file = os.path.join(pdf_directory, filename)
        doc = fitz.open(pdf_file)

        # Initialize flags to check if we should extract the next line as a name or tracking number
        extract_name = False
        extract_tracking_number = False

        # Initialize variables to store the current name and tracking number
        current_name = ""
        current_tracking_number = ""

        # Iterate through each page of the PDF
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text("text")

            # Split the page text into lines
            lines = page_text.split('\n')

            # Iterate through the lines to find the lines that contain shipping info
            for line in lines:
                if "FedEx Priority Overnight" in line or "FedEx Freight Economy" in line or "FedEx 2Day" in line or "FedEx Standard Overnight" in line:
                    extract_name = True
                elif extract_name:
                    # Assume the name is in uppercase
                    if line.strip().isupper():
                        current_name = line.strip()
                        extract_name = False
                        extract_tracking_number = True
                elif extract_tracking_number:
                    # Assume the tracking number is numeric
                    if line.strip().isdigit():
                        current_tracking_number = line.strip()
                        all_names.append(current_name)
                        all_tracking_numbers.append(current_tracking_number)
                        extract_tracking_number = False

        # Close the PDF file
        doc.close()

# Create and save the extracted names and tracking numbers in an Excel file
output_excel_file = r'C:\Users\beckett.mcfarland\Documents\output_excel_files\extracted_names_and_tracking.xlsx'
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['Name', 'Tracking Number'])

for name, tracking_number in zip(all_names, all_tracking_numbers):
    ws.append([name, tracking_number])

wb.save(output_excel_file)
print(f'Extracted names and tracking numbers saved to {output_excel_file}')
