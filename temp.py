import pandas as pd

# Assuming your Excel file is named 'your_file.xlsx' and the columns are named 'employee' and 'lodging'
excel_file_path = 'your_file.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file_path)

# Create a DataFrame with all unique 'employee' values
all_employees = pd.DataFrame(df['employee'].unique(), columns=['employee'])

# Merge with the original DataFrame to include all names, even those with 'lodging' <= 1
result = pd.merge(all_employees, df[df['lodging'] > 1].groupby('employee').size().reset_index(name='Count'), how='left', on='employee')

# Replace NaN values with 0
result['Count'] = result['Count'].fillna(0)

# Create a new Excel writer object
with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a') as writer:
    # Write the result to a new sheet named 'results'
    result.to_excel(writer, sheet_name='results', index=False)
