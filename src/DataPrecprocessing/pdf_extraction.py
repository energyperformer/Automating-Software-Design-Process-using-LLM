import pdfplumber
import os

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a  PDF file.

    Args:
    pdf_path (str): Path to the PDF file.

    Returns:
    str: Extracted text from all pages of the PDF.
    
    """
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
        return text

def extract_all_pdfs(input_folder, output_folder):
    """
    Extract text from all PDF files in the input folder and save as text files in the output folder.

    Args:
    input_folder (str): Path to the folder containing PDF files.
    output_folder (str): Path to the folder where extracted text files will be saved.
    """
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    
    for pdf_file in os.listdir(input_folder):
        
        if pdf_file.endswith(".pdf"):
           
            pdf_path = os.path.join(input_folder, pdf_file)
           
            extracted_text = extract_text_from_pdf(pdf_path)
            output_file = os.path.join(output_folder, pdf_file.replace(".pdf", ".txt"))
            with open(output_file, "w") as f:
                f.write(extracted_text)

if __name__ == "__main__":
    extract_all_pdfs('data/raw/', 'data/processed/')
