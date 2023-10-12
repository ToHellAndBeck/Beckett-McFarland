import pandas as pd
from datetime import datetime, timedelta
import os
# Load the Excel sheet
excel_file_path = r"L:\Warehouse\Freight shipping.xlsx"  # Replace with your Excel file path
df = pd.read_excel(excel_file_path)

# Calculate the date for the day before
previous_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Filter entries for the day before and onwards
new_entries = df[df['Date'] >= previous_date]  # Assuming 'Collectiondate' is the column containing the date

# Check if there are new entries since the day before
if not new_entries.empty:
    # Create the output directory if it doesn't exist
    output_dir = r'C:\Users\beckett.mcfarland\Documents\output_excel_files'  # Replace with your desired directory
    os.makedirs(output_dir, exist_ok=True)

    # Save new entries to an Excel file
    output_excel_file = os.path.join(output_dir, 'New_Freight.xlsx')  # Updated file name to 'new_entries.xlsx'
    new_entries.to_excel(output_excel_file, index=False)
    print('New entries saved to', output_excel_file)
else:
    print('No new entries since', previous_date)
