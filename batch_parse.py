import os
import fitz  # PyMuPDF
from dotenv import load_dotenv

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_upstage.embeddings import UpstageEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# 1. 환경 변수 로드 (.env에 키들 있어야 함)
load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "dream-papers"

assert UPSTAGE_API_KEY, ".env에 UPSTAGE_API_KEY가 필요합니다."
assert QDRANT_URL and QDRANT_API_KEY, "Qdrant 설정이 누락되었습니다."

# 2. Qdrant 연결 및 임베딩 모델 설정
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
embedding_model = UpstageEmbeddings(api_key=UPSTAGE_API_KEY, model="embedding-passage")

# 3. 텍스트 분할기 (500자 기준 청크)
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)

# 4. PDF 파일이 들어있는 폴더 경로
PDF_DIR = r"C:\\Users\\SIM\\Desktop\\pdf"
all_chunks = []

# 5. PDF → 텍스트 → 청크 + 메타데이터 처리
for filename in os.listdir(PDF_DIR):
    if not filename.lower().endswith(".pdf"):
        continue

    pdf_path = os.path.join(PDF_DIR, filename)
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()

    title = os.path.splitext(filename)[0]  # 파일명에서 .pdf 제거

    # 청크 생성 + 각 청크에 메타데이터 추가
    chunks = splitter.create_documents([text], metadatas=[{
        "title": title,
        "source": filename
    }])
    all_chunks.extend(chunks)

print(f"총 청크 수: {len(all_chunks)}")

# Qdrant에 컬렉션이 없으면 생성
existing_collections = qdrant_client.get_collections().collections
existing_names = [c.name for c in existing_collections]

if COLLECTION_NAME not in existing_names:
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=4096,  # Upstage 임베딩 차원 수
            distance=Distance.COSINE
        )
    )
    print(f"Qdrant 컬렉션 생성됨: {COLLECTION_NAME}")
else:
    print(f"Qdrant 컬렉션 존재 확인됨: {COLLECTION_NAME}")

# 6. Qdrant 업로드
# qdrant_client.delete_collection(COLLECTION_NAME)

vectorstore = QdrantVectorStore.from_documents(
    documents=all_chunks,
    embedding=embedding_model,
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    collection_name=COLLECTION_NAME,
    force_recreate=True  #기존 컬렉션 삭제하고 새로 생성
)

vectorstore.add_documents(all_chunks)

print(f"Qdrant 업로드 완료! 컬렉션: {COLLECTION_NAME}")
