# parser.py - Reads PDF files and extracts text from them
import fitz  # fitz is the PyMuPDF library

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Takes a PDF file as bytes and returns all the text inside it.
    Think of it like opening a PDF and copying all the text.
    """
    # Open the PDF from memory (not from disk)
    pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
    
    full_text = ""
    
    # Loop through every page and extract text
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        full_text += page.get_text()
    
    return full_text.strip()