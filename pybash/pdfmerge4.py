import os
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdf2image import convert_from_path
import tempfile
import sys

iteration = sys.argv[1]

def merge_pdfs_to_single_page(pdf_files, output_path, per_row, per_column):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    # Calculate each image size
    img_width = width / per_row
    img_height = height / per_column

    for index, pdf_file in enumerate(pdf_files):
        print(f'Processing {pdf_file}')
        # Convert the first page of the PDF to an image
        images = convert_from_path(pdf_file, first_page=1, last_page=1)
        if images:
            image = images[0]

            # Save image to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                image.save(tmp, format='PNG')
                temp_image_path = tmp.name

            # Calculate position
            row = index % per_row
            column = index // per_row
            x = img_width * row
            y = height - img_height * (column + 1)

            # Draw the image on the canvas
            c.drawImage(temp_image_path, x, y, width=img_width, height=img_height, mask='auto')

            # Delete the temporary file
            os.remove(temp_image_path)

    c.save()

# Example usage
pdf_files = [f"sys{i}/scatter_max_deviation_{i}.pdf" for i in range(8) if os.path.exists(f"sys{i}/hist_max_deviation_{i}.pdf")]
print(pdf_files)
print(f"number of pdf files {len(pdf_files)}")

output_pdf_path = f"scatter_merged_single_page_{iteration}.pdf"
merge_pdfs_to_single_page(pdf_files, output_pdf_path, per_row=4, per_column=4)

