import qrcode

def read_numbers_from_file(file_path):
    with open(file_path, 'r') as file:
        numbers = [int(line.strip()) for line in file if line.strip()]
    return numbers

def generate_qr_codes(numbers, output_folder=r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Tablet Checkout Sheet\QR Codes"):
    for number in numbers:
        data = str(number)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        filename = f"{output_folder}/{number}.png"
        img.save(filename)
        print(f"QR Code for {number} generated and saved as {filename}")

if __name__ == "__main__":
    input_file_path = r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\General Tools\Tablet Numbers.txt"
    numbers_to_encode = read_numbers_from_file(input_file_path)

    generate_qr_codes(numbers_to_encode)
