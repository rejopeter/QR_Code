"""
main.py
--------
Generates QR codes for each URL in a CSV file and inserts them into a Word template
along with other placeholders from the CSV. The filled documents are saved into the 'docs' folder.
"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="docxcompose")
import pandas as pd
import qrcode
from qrcode import constants
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from io import BytesIO
import sys
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm

def generate_qr_image(url, doc, width_mm=40):
    """
    Generate a QR code for the given URL and return an InlineImage compatible with docxtpl.
    
    Parameters:
    - url (str): The data or URL to encode in the QR code.
    - doc (DocxTemplate): The Word template object, required for InlineImage.
    - width_mm (float): Width of the QR code image in millimeters (default 40mm).
    
    Returns:
    - InlineImage: QR code image ready to insert into the template.
    """
    # Create QRCode object with high error correction
    qr = qrcode.QRCode(version=None, error_correction=constants.ERROR_CORRECT_H)
    qr.add_data(url)  # Add URL/data to QR
    qr.make(fit=True)  # Automatically determine QR code size
    # Generate QR code image with rounded modules
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    # Save image to in-memory bytes buffer
    byte_io = BytesIO()
    img.save(byte_io, format='PNG')
    byte_io.seek(0)  # Reset buffer pointer
    # Return as InlineImage for docxtpl
    return InlineImage(doc, byte_io, width=Mm(width_mm))

def main():
    # Check command-line arguments
    # Expecting: python main.py <CSV file> <Word template>
    if len(sys.argv) < 3:
        print("Usage: python main.py yourfile.csv template.docx")
        sys.exit(1)

    csv_file = sys.argv[1]  # Path to input CSV file
    template_file = sys.argv[2]  # Path to Word template

    # Ensure output folder exists
    if not os.path.exists('docs'):
        os.makedirs('docs')

    # Read the CSV into a DataFrame
    # CSV should contain 'name' and 'url' columns, plus other placeholder columns
    df = pd.read_csv(csv_file)

    # Process each row in the CSV
    for index, row in df.iterrows():
        name = row['name']  # File name for the generated Word document
        url = row['url']    # URL/data to encode as QR code

        # Load Word template for this row
        doc = DocxTemplate(template_file)

        # Generate QR code image for insertion into template
        qr_image = generate_qr_image(url, doc)

        # Build context dictionary for template placeholders
        # All CSV columns except 'name' and 'url' are used as template variables
        context = {k: v for k, v in row.items() if k not in ('name', 'url')}
        context['qrcode'] = qr_image  # Add QR code to context

        # Fill in template placeholders with context values
        doc.render(context)

        # Save the filled document to the output folder
        output_doc = f"docs/{name}.docx"
        doc.save(output_doc)
        print(f"Saved {output_doc}")  # Confirmation message

if __name__ == "__main__":
    # Entry point: run main function
    main()