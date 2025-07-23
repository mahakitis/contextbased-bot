from PyPDF2 import PdfReader
import io
import base64

def process_pdf_upload(file_or_base64):
    if hasattr(file_or_base64, 'read'):
        pdf_bytes = file_or_base64.read()
    else:
        pdf_bytes = base64.b64decode(file_or_base64)

    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text
