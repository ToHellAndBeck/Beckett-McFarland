import os

# Directory containing the extracted numbers text file
numbers_directory = r"C:\Users\Beckett.mcfarland\Documents"  # Replace with the actual directory path

# Read the extracted numbers from the text file
numbers_file_path = os.path.join(numbers_directory, 'extracted_numbers.txt')
numbers = []
with open(numbers_file_path, 'r') as numbers_file:
    lines = numbers_file.readlines()
    for line in lines:
        numbers.append(float(line.strip()))

# Create and save the formatted text for each number pair in a separate .dat file
pair_count = len(numbers) // 2
for i in range(pair_count):
    pair_numbers = numbers[i*2:i*2+2]

    # Generate the formatted text
    formatted_text = f'walls=4\n'
    formatted_text += f'w={pair_numbers[0]},a=False,r=0.0,h=0,m=0.0,f=0.0,c=False,cf=1.0,cd=180.0,cs=12\n'
    formatted_text += f'w={pair_numbers[1]},a=False,r=90.0,h=0,m=0.0,f=0.0,c=False,cf=1.0,cd=180.0,cs=12'
    formatted_text += f'w=-{pair_numbers[0]},a=False,r=0.0,h=0,m=0.0,f=0.0,c=False,cf=1.0,cd=180.0,cs=12\n'
    formatted_text += f'w=-{pair_numbers[1]},a=False,r=90.0,h=0,m=0.0,f=0.0,c=False,cf=1.0,cd=180.0,cs=12'

    # Save the formatted text to a .dat file
    dat_file_path = os.path.join(numbers_directory, f'pair_{i+1}.dat')
    with open(dat_file_path, 'w') as dat_file:
        dat_file.write(formatted_text)

    print(f'Pair {i+1} saved to {dat_file_path}')
