from pypdf import PdfReader
from io import BytesIO

def PdfToString(path):
    pdf_file = BytesIO(path)  # 바이트 코드를 파일 객체로 변환
    reader = PdfReader(pdf_file)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = ""
    for i in range(10):
        page = reader.pages[i]
        text += page.extract_text()
    return text