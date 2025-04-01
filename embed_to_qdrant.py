import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_upstage.embeddings import UpstageEmbeddings
from langchain_core.documents import Document
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

# 1. 환경변수 로드
load_dotenv()
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
assert UPSTAGE_API_KEY, "❌ UPSTAGE_API_KEY가 .env에 설정되어 있어야 합니다!"

# 2. 텍스트 파일 경로
TEXT_DIR = Path(r"C:\Users\SIM\Desktop\pdftxt")
assert TEXT_DIR.exists(), "❌ pdftxt 폴더가 존재하지 않습니다!"

# 3. 텍스트 → Document (chunk 분할 포함)
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
            documents.append(Document(page_content=chunk, metadata={"source": str(file_path.name)}))

print(f"✅ 총 {len(documents)}개의 문서를 로딩했습니다.")

# 4. Upstage 임베딩 (4096 차원 모델)
embedding_model = UpstageEmbeddings(
    api_key=UPSTAGE_API_KEY,
    model="embedding-passage"
)

# 5. Qdrant 클라이언트 & 컬렉션 재생성
qdrant_client = QdrantClient(host="localhost", port=6333)

qdrant_client.recreate_collection(
    collection_name="dream-papers",
    vectors_config=VectorParams(size=4096, distance=Distance.COSINE)  # ✅ 차원 주의
)

# 6. Qdrant 벡터 저장소 초기화
qdrant = QdrantVectorStore(
    collection_name="dream-papers",
    client=qdrant_client,
    embedding=embedding_model
)

# 7. Qdrant에 문서 추가
for document in documents:
    qdrant.add_texts(
        texts=[document.page_content],
        metadatas=[document.metadata]
    )

print("✅ Qdrant에 임베딩 완료!")
