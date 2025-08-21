import pandas as pd  # For reading CSV files easily
import qrcode  # For generating QR codes
from qrcode import constants  # For error correction constants
from qrcode.image.styledpil import StyledPilImage  # For styled QR code
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer  # For rounded QR modules
from docx import Document  # To work with Word documents
from docx.shared import Inches  # To set image sizes in Word
import sys
from io import BytesIO
import os

def generate_qr_image(url):
    """
    Generate a QR code for the given URL and return it as an in-memory PNG image.
    Uses styled QR with rounded modules.
    """
    qr = qrcode.QRCode(
        version=None,  # Automatically determine size
        error_correction=constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,  # Size of each box in pixels
        border=4,  # Border width
    )
    qr.add_data(url)
    qr.make(fit=True)
    # Create styled image with rounded modules
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    # Save QR code to in-memory bytes (BytesIO)
    byte_io = BytesIO()
    img.save(byte_io, format='PNG')
    byte_io.seek(0)
    return byte_io

def replace_placeholders(doc, row, qr_image):
    """
    Replace all placeholders in the Word document.
    - For all columns except 'name' and 'url', replace {{column_name}} with value.
    - Replace {{qrcode}} with the QR code image.
    """
    # Collect placeholder columns
    placeholders = {k: v for k, v in row.items() if k not in ('name', 'url')}

    # Replace placeholders in paragraphs
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            for key, value in placeholders.items():
                placeholder = f"{{{{{key}}}}}"  # e.g., {{botanical_name}}
                if placeholder in run.text:
                    run.text = run.text.replace(placeholder, str(value))
            if '{{qrcode}}' in run.text:
                run.text = ''
                run.add_picture(qr_image, width=Inches(1.5))

    # Replace placeholders in tables
    for table in doc.tables:
        for row_cells in table.rows:
            for cell in row_cells.cells:
                for paragraph in cell.paragraphs:
                    for key, value in placeholders.items():
                        placeholder = f"{{{{{key}}}}}"
                        if placeholder in paragraph.text:
                            paragraph.text = paragraph.text.replace(placeholder, str(value))
                    for run in paragraph.runs:
                        if '{{qrcode}}' in run.text:
                            run.text = ''
                            run.add_picture(qr_image, width=Inches(1.5))

def main():
    # Ensure CSV file and template file are provided as command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python main.py yourfile.csv template.docx")
        sys.exit(1)

    csv_file = sys.argv[1]  # Path to CSV file containing URL, botanical_name, family_name, name
    template_file = sys.argv[2]  # Path to Word template file

    # Create output folder 'docx' if it does not exist
    if not os.path.exists('docx'):
        os.makedirs('docx')

    # Read CSV using pandas
    df = pd.read_csv(csv_file)

    # Loop over each row in the CSV
    for index, row in df.iterrows():
        url = row['url']  # URL for QR code
        name = row['name']  # Output DOCX file name

        # Generate QR code image for this URL
        qr_image = generate_qr_image(url)

        # Open Word template
        doc = Document(template_file)

        # Replace all placeholders in the document based on CSV row
        replace_placeholders(doc, row, qr_image)

        # Save the filled document to the 'docx' folder
        output_doc = f"docx/{name}.docx"
        doc.save(output_doc)
        print(f"Saved {output_doc}")  # Confirmation message

if __name__ == "__main__":
    # Entry point of the script
    main()