from docx import Document
import sys, os
import glob

def combine_docx_from_folder(folder, output_file="combined.docx"):
    """
    Combine all .docx files from a folder into a single Word document.
    Files are combined in alphabetical order.
    """
    files = sorted(glob.glob(os.path.join(folder, "*.docx")))
    if not files:
        raise ValueError(f"No .docx files found in {folder}")

    print(f"Found {len(files)} files. Combining into {output_file}...")

    # Start with the first document
    master = Document(files[0])

    for file in files[1:]:
        sub_doc = Document(file)
        master.add_page_break()
        for element in sub_doc.element.body:
            master.element.body.append(element)

    master.save(output_file)
    print(f"✅ Combined document saved as {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python combine_docx.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid folder")
        sys.exit(1)

    combine_docx_from_folder(folder_path, "combined.docx")