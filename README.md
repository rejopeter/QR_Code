# QR Code & Document Automation

This project automates the creation of **custom-branded QR codes**, embeds them into Word documents from a CSV dataset, and converts them into **PDFs**. It removes repetitive manual work by handling QR code generation, document population, and PDF conversion in one streamlined workflow.

---

## ✨ Features

- Generate **single or batch QR codes** from command-line or CSV input.
- Support for **multiple QR styles**:
  - **Jignasa** → Green QR on cream background with Jignasa logo.
  - **Vishwanath** → Yellow QR on dark green background with Vishwanath logo.
- Embed CSV data into a **Word template (`.docx`)** with placeholders.
- Convert generated Word documents into **high-resolution PDFs**.
- Fully **command-line driven** for efficient batch processing.

---

## 📂 Folder Structure

```
QR_Code/
├── main.py          # Master script for batch generation and style selection
├── jignasaQR.py     # Jignasa branded QR code generator
├── vishwanathQR.py  # Vishwanath branded QR code generator
├── DocxToPdf.py     # Converts Word documents to PDFs
├── template.docx    # Word template with placeholders
├── data.csv         # Input CSV dataset
├── docs/            # Output folder for generated Word files
├── final/           # Output folder for generated PDF files
├── assets/          # Images and logos
│   ├── jignasa.png      # Jignasa logo for QR branding
│   ├── vishwanath.png   # Vishwanath logo for QR branding
│   └── ...              # Other images or assets
```

---

## ⚡ Usage

---

### 1. Generate a Single QR Code (branded style)

**Jignasa style**
```bash
python jignasaQR.py <name> <url>
```

**Vishwanath style**
```bash
python vishwanathQR.py <name> <url>
```

**Example:**
```bash
python jignasaQR.py myqr https://example.com
```
Produces `myqr.png` in Jignasa branding.

---

### 2. Batch Document Generation from CSV

1. Place `template.docx` and `data.csv` in the project root.
2. Run `main.py`, specifying the QR style to use:

```bash
python main.py data.csv template.docx jignasa
# or
python main.py data.csv template.docx vishwanath
```

3. Generated `.docx` files will appear in the `docs/` folder.

---

### 3. Convert Word Documents to PDF

```bash
python DocxToPdf.py
```
All `.docx` files in `docs/` will be converted into PDFs in `final/`.

---

### 📑 CSV Format

- **Mandatory columns:**
  - `name` → Output file name for Word document.
  - `url` → Data encoded in QR code.
- **Optional columns:** Match placeholders in the Word template.

**Example `data.csv`:**
```csv
name,url,botanicalname,familyname
Tulsi,https://example.com/tulsi,Ocimum sanctum,Lamiaceae
Neem,https://example.com/neem,Azadirachta indica,Meliaceae
```

---

### 📝 Word Template Placeholders

Use double curly braces in the Word template to mark placeholders:

```
Name: {{name}}
Botanical Name: {{botanicalname}}
Family: {{familyname}}
QR Code: {{qrcode}}
```

---

### 🎨 Example QR Styles

**Jignasa QR**

![Jignasa QR Example](assets/jignasasampleQR.png)

**Vishwanath QR**

![Vishwanath QR Example](assets/vishwanathsampleQR.png)

---

## ⚙️ Requirements

- Python 3.x
- pandas
- docxtpl
- qrcode[pil]
- python-docx
- Pillow

**Install dependencies:**
```bash
pip install pandas qrcode[pil] python-docx docxtpl
```

---

## 🛠 Notes

- QR codes are generated at 300 dpi resolution.
- `main.py` requires a style argument: `jignasa` or `vishwanath`.
- Ensure the template contains `{{qrcode}}` for insertion.
- Avoid special characters in the `name` column (filenames).

---

## 🐞 Troubleshooting

- `ModuleNotFoundError` → Run: `pip install pandas qrcode[pil] python-docx docxtpl`
- Style error → Ensure you pass `jignasa` or `vishwanath` as the 3rd argument to `main.py`.
- Logos missing → Ensure `jignasa.png` or `vishwanath.jpg` are in the project folder.
- QR not appearing → Verify `{{qrcode}}` exists in `template.docx`.
- Permission denied → Ensure you have write access to `docs/` and `final/`.

---

## 📚 References

- [qrcode Python library](https://pypi.org/project/qrcode/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [QR Code – Wikipedia](https://en.wikipedia.org/wiki/QR_code)

---

## 📜 License

Apache License 2.0 © 2025 Dr. J. R. Rejo Peter, BAMS

---