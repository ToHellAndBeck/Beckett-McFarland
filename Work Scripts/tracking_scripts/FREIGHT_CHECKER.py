import pandas as pd
import os

freight_shipping = r"L:\Warehouse\Freight shipping.xlsx"
df2 = pd.read_excel(freight_shipping)

# Assuming 'ShippingType' is the column that indicates the type of shipping
# We filter df2 for entries where this column contains the string 'Freight'
freight_df = df2[df2['Carrier'] == 'Fedex']

print(freight_df.columns)

# Specify the date you are interested in
certain_date = '2023-10-10'  # Replace with your desired date

# Specify the job numbers you are interested in
job_number = '52648'  # Replace with the job number

# Assuming 'Job/PO Number' is the job number column and 'Date' is the date column in df2
# Filter entries for the specified job number and after the certain date
filtered_entries = freight_df[(freight_df['Job/PO Number'] == job_number) & 
                              (pd.to_datetime(freight_df['Date']) >= pd.to_datetime(certain_date))]

# Check if there are filtered entries
if not filtered_entries.empty:
    # Create the output directory if it doesn't exist
    output_dir = r'C:\Users\beckett.mcfarland\Desktop\output_excel_files'  # Replace with your desired directory
    os.makedirs(output_dir, exist_ok=True)

    # Save filtered entries to an Excel file
    output_excel_file = os.path.join(output_dir, f'Freight Shipping {certain_date}.xlsx')  # Updated file name
    filtered_entries.to_excel(output_excel_file, index=False)
    print('Filtered entries saved to', output_excel_file)
else:
    print('No matching entries for the specified job number and date.')
