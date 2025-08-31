"""
main.py
--------
Generates QR codes for each URL in a CSV file and inserts them into a Word template
along with other placeholders from the CSV. The filled documents are saved into the 'docs' folder.
"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="docxcompose")
import pandas as pd
from jignasaQR import generate_jignasa_qr
from vishwanathQR import generate_vishwanath_qr
from io import BytesIO
import sys
import os
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm


def generate_qr_image(url, doc, style="jignasa", width_mm=40):
    """
    Generate a QR code for the given URL and return an InlineImage compatible with docxtpl.
    
    Parameters:
    - url (str): The data or URL to encode in the QR code.
    - doc (DocxTemplate): The Word template object, required for InlineImage.
    - style (str): 'jignasa' or 'vishwanath' (QR style).
    - width_mm (float): Width of the QR code image in millimeters (default 40mm).
    
    Returns:
    - InlineImage: QR code image ready to insert into the template.
    """
    if style == "jignasa":
        img = generate_jignasa_qr(url)
    elif style == "vishwanath":
        img = generate_vishwanath_qr(url)
    else:
        raise ValueError("Invalid QR style. Use 'jignasa' or 'vishwanath'.")

    # Save image to in-memory bytes buffer
    byte_io = BytesIO()
    img.save(byte_io, format="PNG")
    byte_io.seek(0)  # Reset buffer pointer

    return InlineImage(doc, byte_io, width=Mm(width_mm))


def main():
    # Check command-line arguments
    # Expecting: python main.py <CSV file> <Word template> <style>
    if len(sys.argv) < 4:
        print("Usage: python main.py yourfile.csv template.docx <jignasa|vishwanath>")
        sys.exit(1)

    csv_file = sys.argv[1]       # Path to input CSV file
    template_file = sys.argv[2]  # Path to Word template
    style = sys.argv[3].lower()  # QR style

    if style not in ("jignasa", "vishwanath"):
        print("Error: style must be 'jignasa' or 'vishwanath'")
        sys.exit(1)

    # Ensure output folder exists
    if not os.path.exists("docs"):
        os.makedirs("docs")

    # Read the CSV into a DataFrame
    df = pd.read_csv(csv_file)

    # Process each row in the CSV
    for _, row in df.iterrows():
        name = row["name"]  # File name for the generated Word document
        url = row["url"]    # URL/data to encode as QR code

        # Load Word template
        doc = DocxTemplate(template_file)

        # Generate QR code based on chosen style
        qr_image = generate_qr_image(url, doc, style)

        # Build context dictionary
        context = {k: v for k, v in row.items() if k not in ("name", "url")}
        context["qrcode"] = qr_image

        # Render and save
        doc.render(context)
        output_doc = f"docs/{name}.docx"
        doc.save(output_doc)
        print(f"Saved {output_doc}")


if __name__ == "__main__":
    main()