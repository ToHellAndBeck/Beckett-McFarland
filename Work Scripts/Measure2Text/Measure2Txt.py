from app.core import pdf_to_dat

output_file_path = r"C:\Users\beckett.mcfarland\Desktop\Beckett-McFarland\Work Scripts\Measure2Text\output\measurements.txt"

with open(output_file_path, "w") as output_file:
    # Iterate over the PDFs and extract measurements
    for pdf_path in pdf_to_dat.get_new_pdfs():
        pdf = pdf_to_dat.load_pdf(pdf_path)
        for page in pdf.pages:
            page_data = pdf_to_dat.get_page_text(page)
            for idx, line_of_text in enumerate(page_data):
                if pdf_to_dat.is_dimension_location_line(line_of_text):
                    dimension_location = pdf_to_dat.get_dimension_location_from_line(line_of_text)
                    dimension_location_values_text = page_data[idx + 1]
                    dimension_location_data = pdf_to_dat.convert_dimension_text_2_object(dimension_location_values_text)
                    print(f"PDF Path: {pdf_path}", file=output_file)
                    print(f"Location: {dimension_location}", file=output_file)
                    print("Measurements:", file=output_file)
                    for key, value in dimension_location_data.items():
                        print(f"{key}: {value}", file=output_file)
                    print("", file=output_file)  # Empty line

        pdf_to_dat.move_pdf(pdf_path)
