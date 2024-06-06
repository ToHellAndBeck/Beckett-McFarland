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
    [10:55 AM] CJ Ewell
    Team 3 Andrew windham Holiday Inn

    11120 Moriah Drive Fort Worth, Texas 76177 United States

    needs 940 needs 20 sfp 10 gig sent to hotel saturday delivery
    
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

