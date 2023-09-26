import pandas as pd
from datetime import datetime, timedelta

# Load the Excel sheet
excel_file_path = r"L:\Public\Lowell Warehouse Shipping\Parcel Shipping.xlsm"  # Replace with your Excel file path
df = pd.read_excel(excel_file_path)

# Calculate the date for the day before
previous_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Filter entries for the day before and onwards
new_entries = df[(df['Collectiondate'] >= previous_date) & (df['PackageReference2'] == 52648)]  # Adjust column names accordingly

# Check if there are new entries since the day before
if not new_entries.empty:
    # Save new entries to a new Excel file
    output_excel_path = r'C:\Users\beckett.mcfarland\Documents\output_excel_files\New_Parcel.xlsx'  # Replace with your desired output Excel file path
    new_entries.to_excel(output_excel_path, index=False)
    print('New entries saved to', output_excel_path)
else:
    print('No new entries since', previous_date)
