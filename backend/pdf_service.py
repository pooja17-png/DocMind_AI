from pypdf import PdfReader

def extract_text(file):

    pdf = PdfReader(file)

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text