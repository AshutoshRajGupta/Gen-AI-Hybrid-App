# modules/utils.py
import PyPDF2

def load_file(file) -> str:
    """Load text from TXT or PDF file."""
    text = ""
    if file.name.endswith(".txt"):
        text = file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    else:
        raise ValueError("Unsupported file format. Only .txt and .pdf allowed.")
    return text
