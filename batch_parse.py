import os
from dotenv import load_dotenv
from langchain_upstage.document_parse import UpstageDocumentParseLoader

# 🔑 .env 파일에서 API 키 불러오기
load_dotenv()
api_key = os.getenv("UPSTAGE_API_KEY")

# 📁 PDF 폴더 경로
PDF_DIR = r"C:\Users\SIM\Desktop\pdf"

# 📄 PDF 파일 리스트 얻기
pdf_files = [
    os.path.join(PDF_DIR, filename)
    for filename in os.listdir(PDF_DIR)
    if filename.endswith(".pdf")
]

# 📚 문서 파서 초기화
loader = UpstageDocumentParseLoader(
    file_path=pdf_files,
    split="none",              # "page"로 하면 페이지 단위 분할
    output_format="text",      # 또는 "html"
    api_key=api_key            # ✅ .env에서 불러온 키
)

# 📄 문서 파싱 실행
docs = loader.load()

# 📁 결과 저장
for i, doc in enumerate(docs):
    output_path = f"parsed_output_{i+1}.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(doc.page_content)
