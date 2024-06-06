import fitz  # PyMuPDF
import os

def save_page_to_folder(pdf, page, folder):
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Define the output filename
    output_filename = os.path.join(folder, f'page_{page.number + 1}.pdf')

    # Create a new PDF to insert the page
    doc = fitz.open()  # New blank PDF document
    doc.insert_pdf(pdf, from_page=page.number, to_page=page.number)  # Insert the page
    doc.save(output_filename)  # Save the new PDF
    doc.close()  # Close the new PDF

def sort_pages_into_folders(pdf_path, pre_keywords, post_keywords):
    # Open the PDF file
    pdf = fitz.open(pdf_path)

    # Iterate through each page
    for page in pdf:
        # Extract text from the page
        text = page.get_text()

        # Check for pre and post keywords
        if any(keyword.lower() in text.lower() for keyword in pre_keywords):
            save_page_to_folder(pdf, page, 'pre')
        elif any(keyword.lower() in text.lower() for keyword in post_keywords):
            save_page_to_folder(pdf, page, 'post')

    pdf.close()

# Set the path to your PDF file
pdf_path = r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Work Order Verification\work_orders\52648 Switch Refresh WO_2024-01-10.pdf"

# Define your keywords for sorting
pre_keywords = ['Pre-photo']
post_keywords = ['Completed']

# Call the function to sort the pages
sort_pages_into_folders(pdf_path, pre_keywords, post_keywords)
