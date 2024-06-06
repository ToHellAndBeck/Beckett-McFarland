import pandas as pd

# Function to read data from an Excel sheet
def read_excel_sheet(file_path, sheet_name):
    return pd.read_excel(file_path, sheet_name)

# Function to extract shipping information
def extract_shipping_information(data_frame):
    # Replace 'St', 'Ship Date', and 'On site NLT Date' with your column names
    shipping_data = data_frame[['St', 'Ship Date', 'On site NLT Date', 'Carrier Pro']].copy()

    # Filter out rows where 'Carrier Pro' has more than 10 digits
    shipping_data = shipping_data[shipping_data['Carrier Pro'].astype(str).apply(len) <= 10]

    # Convert 'On site NLT Date' and 'Ship Date' columns to datetime
    shipping_data['On site NLT Date'] = pd.to_datetime(shipping_data['On site NLT Date'], errors='coerce')
    shipping_data['Ship Date'] = pd.to_datetime(shipping_data['Ship Date'], errors='coerce')

    # Calculate the number of days it took to arrive, handling NaT values
    shipping_data['Days to Arrive'] = (shipping_data['On site NLT Date'] - shipping_data['Ship Date']).dt.days

    return shipping_data

# Function to write data to a new Excel sheet
def write_to_excel(shipping_data, output_file):
    shipping_data.to_excel(output_file, index=False)

# Main function to orchestrate the process
def main():
    # Replace 'input_file.xlsx' and 'output_file.xlsx' with your file paths
    input_file_path = r"C:\Users\beckett.mcfarland\Documents\Wireless mostly Berkley shipping  (local).xlsx"
    output_file_path = r"C:\Users\beckett.mcfarland\Desktop\Wireless mostly Berkley shipping (output).xlsx"

    # Replace 'Sheet1' with your sheet name
    input_sheet_name = 'Sheet1'

    # Step 1: Read data from the input Excel sheet
    input_data = read_excel_sheet(input_file_path, input_sheet_name)

    # Step 2: Extract shipping information
    shipping_data = extract_shipping_information(input_data)

    # Step 3: Write shipping data to the output Excel sheet
    write_to_excel(shipping_data, output_file_path)

if __name__ == "__main__":
    main()
