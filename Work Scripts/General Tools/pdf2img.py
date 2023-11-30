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
        output_path = os.path.join(output_folder, f"page_{page_number + 1}.jpg")
        pil_image.save(output_path)

    # Close the PDF document
    pdf_document.close()
if __name__ == "__main__":
    # Replace 'input.pdf' with the path to your PDF file
    pdf_path = r'C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Tablet Checkout Sheet\PDFS\Scanned_Documents.pdf'
    
    # Replace 'output_folder' with the desired output folder for JPGs
    output_folder = r'C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Tablet Checkout Sheet\Tablet Pics'

    pdf_to_images(pdf_path, output_folder)
