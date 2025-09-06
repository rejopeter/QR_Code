import qrcode
from qrcode import constants
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import CircleModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask
from PIL import Image
import sys, os


def generate_vishwanath_qr(url, logo_path="assets/vishwanath.jpg", scale_factor=4):
    """
    Generate a high-resolution Vishwanath-styled QR code with logo at center.
    Returns a PIL.Image object.
    """
    if not os.path.exists(logo_path):
        raise FileNotFoundError(f"Logo file not found at {logo_path}")

    # Load logo
    logo = Image.open(logo_path).convert("RGBA")

    # Create QR
    qr = qrcode.QRCode(
        version=None,
        error_correction=constants.ERROR_CORRECT_H,
        box_size=25,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Base QR image with circle modules and custom colors
    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=CircleModuleDrawer(),
        color_mask=SolidFillColorMask(
            front_color=(212, 223, 73),   # yellow-ish
            back_color=(37, 89, 46)       # dark green
        )
    ).convert("RGBA")

    # Upscale for high-res
    high_res = img.resize(
        (img.size[0] * scale_factor, img.size[1] * scale_factor),
        Image.Resampling.LANCZOS
    )

    # Resize logo while keeping aspect ratio
    max_logo_size = high_res.size[0] // 5
    logo.thumbnail((max_logo_size, max_logo_size), Image.Resampling.LANCZOS)

    # Make white background transparent
    datas = logo.getdata()
    newData = [
        (255, 255, 255, 0) if (r > 240 and g > 240 and b > 240) else (r, g, b, a)
        for r, g, b, a in datas
    ]
    logo.putdata(newData)

    # Center logo on QR
    pos = ((high_res.size[0] - logo.size[0]) // 2,
           (high_res.size[1] - logo.size[1]) // 2)
    high_res.paste(logo, pos, mask=logo)

    # Resize final output to 2 cm x 2 cm at 300 DPI
    final_size_px = int(2 / 2.54 * 300)  # 2 cm → inches → pixels
    high_res = high_res.resize((final_size_px, final_size_px), Image.Resampling.LANCZOS)

    return high_res


# Keep CLI support
def main():
    if len(sys.argv) != 3:
        print("Usage: python vishwanathQR.py <output_file_name> <URL>")
        sys.exit(1)

    output_file = sys.argv[1] + ".jpg"
    url = sys.argv[2]

    img = generate_vishwanath_qr(url)

    # Save explicitly with DPI
    img.save(output_file, format="JPEG", dpi=(300, 300), quality=95, optimize=True)
    print(f"High-resolution QR code saved to {output_file} at 300 DPI")


if __name__ == "__main__":
    main()