import pandas as pd
from datetime import datetime, timedelta

# Load the Excel sheet
excel_file_path = r"L:\Warehouse\Freight shipping.xlsx"  # Replace with your Excel file path
df = pd.read_excel(excel_file_path)

# Calculate the date for the day before
previous_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

# Filter entries for the day before and onwards
new_entries = df[df['Date'] >= previous_date]  # Assuming 'Date' is the column containing the date

# Check if there are new entries since the day before
if not new_entries.empty:
    # Create a string to store the new entries
    new_entries_str = new_entries.to_string(index=False)

    # Write new entries to a text file
    text_file_path = r'C:\Users\beckett.mcfarland\Documents\output_excel_files\New_Freight.xlsx'  # Replace with your desired text file path
    with open(text_file_path, 'a') as text_file:
        text_file.write('New entries since {}: \n'.format(previous_date))
        text_file.write(new_entries_str)
        text_file.write('\n\n')
    print('New entries written to', text_file_path)
else:
    print('No new entries since', previous_date)
