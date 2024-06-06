import PyPDF2

def split_pdf_into_pages(input_pdf_path, output_folder):
    # Open the input PDF file
    pdf_file = open(input_pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Create the output folder if it doesn't exist
    import os
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through each page and save it as a separate PDF
    for page_num in range(len(pdf_reader.pages)):
        pdf_writer = PyPDF2.PdfWriter()
        pdf_writer.add_page(pdf_reader.pages[page_num])

        # Create a filename for the page (e.g., page_1.pdf, page_2.pdf, etc.)
        output_file = os.path.join(output_folder, f'page_{page_num + 1}.pdf')

        # Write the page to the output file
        with open(output_file, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

    # Close the input PDF file
    pdf_file.close()


if __name__ == '__main__':
    input_pdf_path = r"C:\Users\beckett.mcfarland\Documents\PDFs\download.pdf"  # Replace with the path to your input PDF file
    output_folder = r'C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\General Tools\PDFS'  # Replace with the folder where you want to save the pages
    output_pdf_path = 'output.pdf'
    split_pdf_into_pages(input_pdf_path, output_folder)
