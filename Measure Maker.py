import fitz  # PyMuPDF
import re
import os

# Directory containing PDF files
pdf_directory = r"C:\Users\Beckett.mcfarland\Downloads"  # Replace with the actual directory path

# Initialize list to store extracted numbers
extracted_numbers = []

# Regular expression pattern to extract numbers (including decimals)
number_pattern = r'(\d+(\.\d+)?)'

# Iterate through each PDF file in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith('_extracted_lines.txt'):
        text_file_path = os.path.join(pdf_directory, filename)

        # Read the content of the text file
        with open(text_file_path, 'r') as text_file:
            lines = text_file.readlines()

        # Extract numbers from each line
        for line in lines:
            numbers = re.findall(number_pattern, line)
            for number_tuple in numbers:
                # Append the first group (the number) to the extracted numbers list
                extracted_numbers.append(float(number_tuple[0]))

# Create and save the extracted numbers in a new text file
output_text_file = os.path.join(pdf_directory, 'extracted_numbers.txt')
with open(output_text_file, 'w') as text_file:
    for num in extracted_numbers:
        text_file.write(f"{num}\n")

print(f'Extracted numbers saved to {output_text_file}')