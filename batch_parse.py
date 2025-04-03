import os
import fitz  # PyMuPDF
from dotenv import load_dotenv

from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_upstage.embeddings import UpstageEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# emotion_analysis.py
from emotion_analysis import process_qdrant_document

# 환경 변수 로드
load_dotenv()
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

assert UPSTAGE_API_KEY, ".env에 UPSTAGE_API_KEY가 필요합니다."
assert QDRANT_URL and QDRANT_API_KEY, "Qdrant 설정이 누락되었습니다."

def process_pdfs(pdf_dir, user_id, title, chunk_size=1000, chunk_overlap=50):
    """
    PDF 폴더 내 모든 PDF를 처리하여 Qdrant에 업로드하고, content를 텍스트로 return하는 함수
    Args:
        pdf_dir (str): PDF 파일이 들어있는 폴더 경로
        user_id: 사용자 id
        chunk_size (int): 텍스트 청크 크기
        chunk_overlap (int): 청크 간 오버랩 크기
    """

    collection_name = f"dream-{user_id}"
    # Qdrant 클라이언트 및 임베딩 모델 설정
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    embedding_model = UpstageEmbeddings(api_key=UPSTAGE_API_KEY,
                                        model="embedding-passage")

    # 텍스트 분할기
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    all_chunks = []

    # PDF → 텍스트 변환 및 청크 생성
    for filename in os.listdir(pdf_dir):
        if not filename.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(pdf_dir, filename)
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        title = os.path.splitext(filename)[0]  # 파일명에서 .pdf 제거

        chunks = splitter.create_documents([text],
                                           metadatas=[{
                                               "title": title,
                                               "source": filename
                                           }])
        all_chunks.extend(chunks)

    print(f"총 청크 수: {len(all_chunks)}")

    # Qdrant 컬렉션 확인 및 생성
    existing_collections = qdrant_client.get_collections().collections
    existing_names = [c.name for c in existing_collections]

    if collection_name not in existing_names:
        qdrant_client.create_collection(collection_name=collection_name,
                                        vectors_config=VectorParams(
                                            size=4096,
                                            distance=Distance.COSINE))
        print(f"Qdrant 컬렉션 생성됨: {collection_name}")
    else:
        print(f"Qdrant 컬렉션 존재 확인됨: {collection_name}")

    # Qdrant에 업로드
    vectorstore = QdrantVectorStore.from_documents(
        documents=all_chunks,
        embedding=embedding_model,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        collection_name=collection_name,
        force_recreate=False  # 기존 컬렉션에 추가됨
    )

    print(f"Qdrant 업로드 완료! 컬렉션: {collection_name}")

    return "\n".join([chunk.page_content for chunk in all_chunks])


# 사용 예시
if __name__ == "__main__":
    PDF_DIR = r"./uploads"
    process_pdfs(PDF_DIR, "test", "ex-title")
