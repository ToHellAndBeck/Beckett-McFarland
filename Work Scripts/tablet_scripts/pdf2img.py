import fitz  # PyMuPDF
from PIL import Image
import os

def pdf_to_images(pdf_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Loop through each page in the PDF
    for page_number in range(pdf_document.page_count):
        # Get the page
        page = pdf_document[page_number]

        # Get the pixel dimensions of the page
        image_matrix = fitz.Matrix(2.0, 2.0)  # Adjust scaling factor as needed

        # Create an image from the page
        image = page.get_pixmap(matrix=image_matrix)

        # Convert the image to a Pillow Image
        pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)

        # Save the image as a JPG file
        output_path = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_{page_number + 1}.jpg")
        pil_image.save(output_path)

    # Close the PDF document
    pdf_document.close()

def convert_all_pdfs(input_folder, output_folder):
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            pdf_to_images(pdf_path, output_folder)

if __name__ == "__main__":
    # Replace 'input_folder' with the path to the folder containing PDFs
    input_folder = r'C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Tablet Checkout Sheet\PDFS\Seperated'
    
    # Replace 'output_folder' with the desired output folder for JPGs
    output_folder = r'C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Tablet Checkout Sheet\Tablet Pics'

    convert_all_pdfs(input_folder, output_folder)
