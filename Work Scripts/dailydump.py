import xlrd
import openpyxl
import os
filepath = r"C:\Users\beckett.mcfarland\Documents"
# Load the source workbook using xlrd
source_workbook = xlrd.open_workbook('copy of Master Switch Report 8-27-23.xlsb')

# Specify the source and destination sheets by name
source_sheet_name = 'Conference Call Switch'
destination_workbook = openpyxl.load_workbook('Switch tracking numbers 8-25-23.xlsb')
destination_sheet_name = 'DAILY DUMP'

# Get the source sheet using xlrd
source_sheet = source_workbook.sheet_by_name(source_sheet_name)

# Get the destination sheet using openpyxl
destination_sheet = destination_workbook[destination_sheet_name]
print(source_sheet.values)
# Copy data from source to destination
# for row_index in range(source_sheet.nrows):
#    for col_index in range(source_sheet.ncols):
#        cell_value = source_sheet.cell(row_index, col_index).value
#       destination_sheet.cell(row=row_index + 1, column=col_index + 1).value = cell_value

# Save the destination workbook
destination_workbook.save('destination.xlsb')

# Close the destination workbook (openpyxl handles source workbook closing)
destination_workbook.close()

print("Data copied and saved to destination.xlsb")
