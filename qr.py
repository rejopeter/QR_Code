import qrcode
from qrcode import constants
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image
import sys, os

def generate_simple_qr(url, size_cm=4):
    """
    Generate a sharp QR code (no logo) at exact size (cm) for 300 DPI print.
    """
    # Target pixels for given cm at 300 DPI
    target_px = int(size_cm / 2.54 * 300)

    # Make QR
    qr = qrcode.QRCode(
        version=None,
        error_correction=constants.ERROR_CORRECT_H,
        box_size=1,   # start small
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Find how many modules wide the QR is
    num_modules = qr.modules_count + 2 * qr.border

    # Compute best box_size to reach ~target_px
    box_size = max(1, target_px // num_modules)
    qr.box_size = box_size  # adjust dynamically

    # Rebuild image
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(),
        color_mask=SolidFillColorMask(
            front_color=(0, 0, 0),
            back_color=(255, 255, 255)
        )
    ).convert("RGB")

    # Final size in pixels
    final_px = img.size[0]

    # Adjust to exactly target_px if needed
    if final_px != target_px:
        img = img.resize((target_px, target_px), Image.Resampling.NEAREST)

    return img

def main():
    if len(sys.argv) != 3:
        print("Usage: python simpleQR.py <output_file_name> <URL>")
        sys.exit(1)

    output_file = sys.argv[1] + ".jpg"
    url = sys.argv[2]

    img = generate_simple_qr(url)

    # Save as JPEG with DPI
    img.save(output_file, format="JPEG", dpi=(300, 300), quality=95, optimize=True)
    print(f"QR code saved to {output_file} at 300 DPI (2 cm x 2 cm)")


if __name__ == "__main__":
    main()