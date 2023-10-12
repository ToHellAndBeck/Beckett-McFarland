import re

def extract_data(message):
    store_number_match = re.search(r'site (\d+)', message)
    store_number = store_number_match.group(1) if store_number_match else None

    notes_match = re.search(r'\[.+\]\s+(.+)\n', message)
    notes = notes_match.group(1) if notes_match else None

    return {
        "Store Number": store_number,
        "Notes": notes,
        "Bill To": "Wachter",  # Assuming "Bill To" is always "Wachter"
        "Shipping Method": "Overnight",  # Assuming shipping method is always "Overnight"
        "Job Number": "52648"  # Assuming a default job number for now
    }

# Input data
input_data = """
[[12:02 PM] CJ Ewell
switch team 8 site 5397 needs 4 power cords for th  ex4600 switches
switch team 12 site 1244 needs 10 sfp 10 gig and 40 lc-sc 3 meter blue jumpers
Switch team 17 site 3572 needs 10 sfp 10 gig

[12:03 PM] CJ Ewell
switch tam carter site 5497 1 roll 1000 ft fiber if not there use 800 and 2 40 gig dac cables

[12:03 PM] CJ Ewell
switch team steve site 605 needs 30 lc-lc 3 meter fiber jumpers

[1:14 PM] CJ Ewell
switch team karl site 280 needs 4 sfp 10 gig
"""

# Split the input into messages
messages = re.split(r'\n(?=\[\d+:\d+ [APM]+\])', input_data.strip())

# Extract and format data from each message
formatted_data_list = []
for msg in messages:
    formatted_data = extract_data(msg)
    if formatted_data["Store Number"]:
        formatted_data_list.append(formatted_data)

# Print the formatted data
for idx, data in enumerate(formatted_data_list, start=1):
    print(f"Data {idx}:")
    print(data)
    print()

