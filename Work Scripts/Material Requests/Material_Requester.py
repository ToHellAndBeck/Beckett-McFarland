import openpyxl

table_data = [

    ["Time", "Sender", "Team", "Site", "Item", "Quantity"],

    ["12:02 PM", "CJ Ewell", "Team 8", "5397", "Power cords for ex4600 switches", "4"],

    ["12:02 PM", "CJ Ewell", "Team 12", "1244", "10 SFP 10 gig, 40 LC-SC 3m jumpers", "10"],

    ["12:02 PM", "CJ Ewell", "Team 17", "3572", "10 SFP 10 gig", "10"],

    ["12:03 PM", "CJ Ewell", "Team Carter", "5497", "1 roll 1000 ft fiber, 800 ft if not available, 2 40 gig DAC cables", "1 roll, 2 cables"],

    ["12:03 PM", "CJ Ewell", "Team Steve", "605", "30 LC-LC 3m fiber jumpers", "30"]

]

import datetime
output_directory = r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Material Requests\Output\\"
today = datetime.datetime.now().date()
key_coordinates = {"Site": (3, 9), "Item": (17, 5), "Quantity": (17, 4)}
headers = []
template_location = r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Material Requests\Template\Walmart Shipping Request Template (Personal).xlsx"
wb = openpyxl.load_workbook(template_location)
ws = wb["Sheet1"]
for row_idx, row in enumerate(table_data):
    
    if row_idx == 0:
        for column in row:
            headers.append(column)
    else:
        name_list = []
        for column_idx, column_value in enumerate(row):
            if column_idx == 2 or column_idx == 3:
                name_list.append(column_value)

            key = headers[column_idx]
            position = key_coordinates.get(key)
            if position:
                row = position[0]
                col = position[1]
                try:
                    column_value = int(column_value)
                except:
                    ...
                ws.cell(row, col).value = column_value
        name_list.append(str(today))
        file_name = output_directory + "-".join(name_list) + ".xlsx"
        wb.save(file_name)

        

