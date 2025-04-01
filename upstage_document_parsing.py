import requests
import fitz  # PyMuPDF
from io import BytesIO


def upstage_document_pasring(filename):
    UPSTAGE_API_KEY = "up_iIFJ3o3pGBZt5KOdlSj2SCDnGizup"  # ex: up_xxxYYYzzzAAAbbbCCC
    UPSTAGE_URL = "https://api.upstage.ai/v1/document-digitization"
    headers = {"Authorization": f"Bearer {UPSTAGE_API_KEY}"}
    files = {"document": open(filename, "rb")}
    data = {"ocr": "force", "base64_encoding": "['table']", "model": "document-parse"}
    response = requests.post(UPSTAGE_URL, headers=headers, files=files, data=data)
    # print(response.json())
    return response.json()

# 웹 pdf를 메모리에 바로 불러와서 읽기
# PyMuPDF 사용
# def web_pdf_reader(pdf_url):
#     # 1. 웹에서 PDF 받아오기
#     # pdf_url = "https://example.com/sample.pdf"  
#     response = requests.get(pdf_url)
    
#     # 2. 메모리에서 PDF 열기
#     pdf_data = BytesIO(response.content)
#     doc = fitz.open(stream=pdf_data, filetype="pdf")
    
#     # 3. 페이지별 텍스트 추출
#     for page in doc:
#         text = page.get_text()
#         print(text)