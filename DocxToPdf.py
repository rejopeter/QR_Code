from docx2pdf import convert  # Import the docx2pdf library to convert Word documents to PDF
import os  # Import os module for folder operations

# Input folder containing DOCX files
input_folder = "docs"

# Output folder where converted PDFs will be saved
output_folder = "final"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Convert all DOCX files in the input folder to PDF
# This will maintain the same file names but with .pdf extension
convert(input_folder, output_folder)

# Print a confirmation message after conversion
print(f"✅ All Word files converted to PDF in '{output_folder}'")