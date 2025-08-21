# QR Code Generator

## Overview
This script generates a QR code image from a provided URL. The QR code is saved as a PNG file with customizable output file name.

## Requirements
- Python 3.x
- `qrcode` library (install via `pip install qrcode[pil]`)

## Usage
Run the script from the command line with the output file name and URL as arguments:

```
python3 generate_qr.py <output_file_name> <URL>
```

## Parameters
- `<output_file_name>`: Name of the output PNG file (without extension).
- `<URL>`: The URL to encode in the QR code.

## Example
```
python generate_qr.py my_qr_code https://www.example.com
```
This command generates a QR code image named `my_qr_code.png` encoding the URL `https://www.example.com`.

![QR Code](my_qr_code.png)

## Notes
- The output file will always have a `.png` extension appended.
- The QR code uses an error correction level of Q, providing a good balance between data recovery and capacity.
- The QR code version is automatically determined based on the length of the URL.
- Ensure the URL is valid and accessible for best results.