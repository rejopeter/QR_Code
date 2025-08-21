import qrcode
from qrcode import constants
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer

import sys

def main():
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python generate_qr.py <output_file_name> <URL>")
        sys.exit(1)

    # Get the output file name and append .png extension
    output_file = sys.argv[1] + ".png"
    # Get the URL to encode in the QR code
    url = sys.argv[2]

    # Create a QRCode object with specified parameters
    qr = qrcode.QRCode(
        version=None,  # automatic size determination
        error_correction=constants.ERROR_CORRECT_Q,  # error correction level
        box_size=10,  # size of each box in pixels
        border=4,  # border size in boxes
    )
    # Add the URL data to the QR code
    qr.add_data(url)
    # Compile the QR code data into a matrix
    qr.make(fit=True)

    # Create an image from the QR code matrix with specified colors
    img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())
    # Save the generated image to the output file
    img.save(output_file)

    # Inform the user that the QR code has been saved
    print(f"QR code saved to {output_file}")

if __name__ == "__main__":
    main()