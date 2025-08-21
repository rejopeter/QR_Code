## qr.py Script
The `qr.py` script generates a single QR code image based on command-line arguments. It accepts:
- `name`: The desired output file name (without extension) for the QR code PNG.  
- `url`: The URL or text to encode in the QR code.  

### Usage
```bash
python qr.py <name> <url>
```

### Example
Generate a QR code for `https://example.com` and save as `myqr.png`:
```bash
python qr.py myqr https://example.com
```
![Example QR Code](myqr.png)

# QR Code & Document Automation Project

## Project Overview
This project allows the generation of a large number of QR codes from a CSV file, embeds additional data into a Word template (`.docx`), and converts the documents to PDFs for various purposes. It simplifies repetitive tasks by automating QR generation, document filling, and PDF conversion.

## Workflow Hierarchy
The project consists of three scripts working together:

```
template.docx, data.csv
          │
          ▼
    main.py script
          │
          ▼
   Generates Word documents (.docx)
          │
          ▼
        docx/ folder
          │
          ▼
    DocxToPdf.py script
          │
          ▼
   Converts all .docx to PDFs
          │
          ▼
        final/ folder
```

## Features
- Generate multiple QR codes from CSV data.  
- Embed CSV data into Word templates with placeholders.   
- Convert Word documents to PDFs efficiently.  
- Fully command-line driven for batch processing.  

## Folder Structure
- `docs/`: Output Word documents generated from CSV and template.  
- `final/`: Output PDFs converted from Word documents.  

## CSV Format
- **Mandatory columns**:  
  - `name`: Output file name for Word document.  
  - `url`: Data to encode in QR code.  
- **Optional columns**: Correspond to placeholders in the Word template (e.g., `botanicalname`, `familyname`).  
- Each row in the CSV generates a corresponding Word document with placeholders filled and a QR code embedded.  

## Word Template Placeholders
- The Word template can include placeholders using `{{placeholder_name}}` format.  
- Example placeholders: `{{botanicalname}}`, `{{familyname}}`, `{{qrcode}}`.  
- Placeholder names should match the CSV column headers (case-insensitive).  

## Requirements
- Python 3.x  
- `pandas`  
- `docxtpl`
- `qrcode[pil]`  
- `python-docx`  
- `Pillow` (installed automatically with `qrcode[pil]`)  

Install dependencies via:
```bash
pip install pandas qrcode[pil] python-docx docxtpl
```

## Usage
1. Place `template.docx` and `data.csv` in the project root folder.  
2. Run the main script to generate Word documents:
```bash
python main.py data.csv template.docx
```
3. Verify alignment and formatting of generated documents in the `docs/` folder.  
4. Convert all Word documents to PDF using:
```bash
python DocxToPdf.py
```

## Examples
Generate Word documents from CSV:
```bash
python main.py data.csv template.docx
```
Convert generated documents to PDF:
```bash
python DocxToPdf.py
```

## Notes
- The QR code will always have a `.png` extension appended.  
- Error correction level H is used, allowing recovery of up to 30% data loss.  
- CSV column names must match Word template placeholders for correct replacement.  
- Verify document alignment before converting to PDF.  
- Avoid special characters in the `name` column to prevent filesystem issues.  

## Troubleshooting
- **ModuleNotFoundError**: Ensure dependencies are installed: `pip install pandas qrcode[pil] python-docx`.  
- **Invalid CSV**: Confirm that mandatory columns `name` and `url` exist.  
- **Permission Denied**: Run scripts with write access to output folders.  
- **QR codes not appearing**: Ensure `{{qrcode}}` placeholder exists in the Word template.  

## References
- [qrcode Python library](https://pypi.org/project/qrcode/)  
- [python-docx Documentation](https://python-docx.readthedocs.io/)  
- [QR Code Wikipedia](https://en.wikipedia.org/wiki/QR_code)