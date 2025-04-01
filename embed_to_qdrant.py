import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_upstage.embeddings import UpstageEmbeddings
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

# 1. 환경 변수 로드
load_dotenv()
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")  # 클라우드 주소
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")  # 클라우드 API 키

assert UPSTAGE_API_KEY and QDRANT_URL and QDRANT_API_KEY, "❌ 환경 변수가 누락되었습니다!"

# 2. 텍스트 폴더 경로
TEXT_DIR = Path(r"C:\Users\SIM\Desktop\pdftxt")
assert TEXT_DIR.exists(), "❌ pdftxt 폴더가 존재하지 않음!"

# 3. 텍스트 -> Document 변환
documents = []
chunk_size = 2000

def split_text(text, chunk_size):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

for file_path in TEXT_DIR.glob("*.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read().strip()
    if text:
        chunks = split_text(text, chunk_size)
        for chunk in chunks:
            documents.append(Document(page_content=chunk, metadata={"source": file_path.name}))

print(f"✅ 총 {len(documents)}개의 문서를 로딩했습니다.")

# 4. Upstage 임베딩
embedding_model = UpstageEmbeddings(api_key=UPSTAGE_API_KEY, model="embedding-passage")

# 5. Qdrant Cloud 클라이언트
qdrant_client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

# 6. 컬렉션 생성 (없으면)
COLLECTION_NAME = "dream-papers"

if not qdrant_client.collection_exists(COLLECTION_NAME):
    print("📌 Qdrant Cloud에 컬렉션이 없어서 새로 생성합니다.")
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=4096, distance=Distance.COSINE)
    )
else:
    print("📂 이미 Qdrant Cloud에 컬렉션이 존재합니다.")

embedding_model = UpstageEmbeddings(
    api_key=UPSTAGE_API_KEY,
    model="embedding-passage",
)

# 7. 벡터 스토어 생성 및 데이터 업로드
qdrant = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embedding=embedding_model,
)

# 8. 문서 추가
qdrant.add_texts(
    texts=[doc.page_content for doc in documents],
    metadatas=[doc.metadata for doc in documents],
)

print("✅ Qdrant Cloud에 업로드 완료!")
