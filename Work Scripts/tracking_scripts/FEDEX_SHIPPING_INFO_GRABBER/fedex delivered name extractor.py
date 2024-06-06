import os
import pdfplumber
import pandas as pd
import re
import openpyxl
import shutil
def parse_pdf_text(text):
    """
    Parse the extracted text from a PDF into a dictionary, matching the columns of the example Excel file.
    """
    # A helper function to get the regex search result or return None
    def get_search_result(pattern, text):
        match = re.search(pattern, text)
        return match.group(1) if match else None

    # Attempt to find the "Signed for by" text and handle if it is not found
    signed_for_by_match = re.search(r'Signed for by:\s*([\w\.\s]+?)(?:\sService|\sDelivery|$)', text)
    signed_for_by = signed_for_by_match.group(1).strip() if signed_for_by_match else None
    delivery_date_pattern = r'Delivery date\s*:?["\s]*([\w\s]+,\s*\d{4}\s+\d{1,2}:\d{2})'
    
    # Search for the delivery date using the regex pattern
    delivery_date_match = re.search(delivery_date_pattern, text)
    
    # Extract the delivery date if a match is found, otherwise set to None
    delivery_date = delivery_date_match.group(1).strip() if delivery_date_match else None

    parsed_data = {
        "Tracking number": get_search_result(r'Tracking number:\s+(\d+)', text),
        "Status": get_search_result(r'Status:\s+(\w+)', text),
        "Signed for by": signed_for_by,
        "Service type": get_search_result(r'Service type:\s+([\w\s]+)\n', text),
        "Special Handling": get_search_result(r'Special Handling:\s+([\w\s;]+)\n', text),
        "Delivered To": get_search_result(r'Delivered To:\s+([\w\s\/]+)\n', text),
        "Delivery date": delivery_date,
        "Ship Date": get_search_result(r'Ship Date:\s+([\w\s,:]+)\n', text),
        "Weight": get_search_result(r'Weight:\s+([\w\s\.\/KG]+)\n', text)
    }
    return parsed_data

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_data = []
        for i, page in enumerate(pdf.pages):
            if i >= 1:  # Skip the first page
                page_text = page.extract_text()
                if page_text:
                    parsed_data = parse_pdf_text(page_text)
                    all_data.append(parsed_data)
        return all_data

def process_pdfs_in_folder(folder_path, output_excel_file):
    # If the Excel file already exists, read it into a DataFrame
    if os.path.exists(output_excel_file):
        existing_df = pd.read_excel(output_excel_file)
    else:
        existing_df = pd.DataFrame()

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            pdf_data = extract_text_from_pdf(pdf_path)
            for data in pdf_data:
                # Create a DataFrame from the current data
                data_df = pd.DataFrame([data])
                # If existing_df is not empty, check for duplicates before appending
                if not existing_df.empty:
                    # Convert tracking number to string to prevent scientific notation in Excel
                    data_df['Tracking number'] = data_df['Tracking number'].astype(str)
                    existing_df['Tracking number'] = existing_df['Tracking number'].astype(str)
                    # Check if the data is not in the existing DataFrame
                    if not any(existing_df.eq(data_df.iloc[0]).all(axis=1)):
                        existing_df = pd.concat([existing_df, data_df], ignore_index=True)
                else:
                    # If existing_df is empty, simply append the data
                    existing_df = pd.concat([existing_df, data_df], ignore_index=True)
            # Move the processed PDF file to the "OLD" folder
            old_folder_path = os.path.join(folder_path, "OLD")
            os.makedirs(old_folder_path, exist_ok=True)
            shutil.move(pdf_path, os.path.join(old_folder_path, filename))
            
    # Save the updated DataFrame to the Excel file
    existing_df.to_excel(output_excel_file, index=False, float_format='%f')


folder_path = r'C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\tracking_scripts\FEDEX_SHIPPING_INFO_GRABBER\PDFS'  # Replace with the path to your folder containing PDFs
output_excel_file = r'C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\tracking_scripts\FEDEX_SHIPPING_INFO_GRABBER\Output\parsed_shipping_info.xlsx'  # Replace with your desired output path
process_pdfs_in_folder(folder_path, output_excel_file)

print(f"Updated data saved to {output_excel_file}")