import fitz  # PyMuPDF
import os

# Function to extract text from PDF
def extract_text_from_pdf(pdf_filename):
    text = ""
    pdf_document = fitz.open(pdf_filename)

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()
    return text

# Function to append text data to the existing TXT file
def append_text_to_txt(text, txt_filename):
    with open(txt_filename, 'a', encoding='utf-8') as txt_file:
        txt_file.write(text)

if __name__ == "__main__":
    pdf_directory = r"C:\Users\beckett.mcfarland\Documents\PDFs"
    txt_filename = r"C:\Users\beckett.mcfarland\Documents\txt_files\output.txt"  # Replace with the desired output TXT file path

    # Check if the output file already exists
    if not os.path.exists(txt_filename):
        # Create the file if it doesn't exist
        with open(txt_filename, 'w', encoding='utf-8'):
            pass

    # Iterate through PDF files in the directory
    for pdf_file in os.listdir(pdf_directory):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, pdf_file)
            pdf_text = extract_text_from_pdf(pdf_path)

            # Append the extracted text to the existing TXT file
            append_text_to_txt(pdf_text, txt_filename)

    print(f"Text from PDFs has been extracted and appended to {txt_filename}")
