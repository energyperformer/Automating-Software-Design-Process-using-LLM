import PyPDF2
def process_srs_document(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def generate_template_from_srs(srs_text):
    """
    Formats the extracted text into a structured template for LLM input.
    """
    template = f"""
    Document Analysis:
    - Key Actors: (Extract explicit actors like 'Admin', 'User')
    - Functional Requirements: (Summarize all system requirements)
    - Non-Functional Requirements: (Summarize non-functional aspects like performance)

    Input SRS Text:
    {srs_text}
    """
    return template