from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import requests
import torch
import json
import uuid
from dotenv import load_dotenv
import os

# ===== 설정 =====
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
EMBEDDING_API_KEY = os.getenv("UPSTAGE_API_KEY")

# ===== 감정 분석 모델 =====
model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

emotion_labels = [
    'admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
    'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
    'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
    'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
    'relief', 'remorse', 'sadness', 'surprise', 'neutral'
]

# ===== 감정 분석 =====
def analyze_emotions(text, threshold=0.3):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.sigmoid(logits).squeeze().tolist()
    results = [
        {"label": label, "score": round(score, 3)}
        for label, score in zip(emotion_labels, probs)
        if score > threshold
    ]
    return sorted(results, key=lambda x: x["score"], reverse=True)

# ===== 텍스트 청크 분할 =====
def split_text_into_chunks(text, max_tokens=4000):
    approx_chunk_size = max_tokens * 4  # 영어 기준 1 token ≈ 4 chars
    return [text[i:i+approx_chunk_size] for i in range(0, len(text), approx_chunk_size)]

# ===== 임베딩 평균 계산 =====
def get_mean_embedding(text):
    chunks = split_text_into_chunks(text)
    vectors = []

    for chunk in chunks:
        url = "https://api.upstage.ai/v1/solar/embeddings"
        headers = {
            'Authorization': f'Bearer {EMBEDDING_API_KEY}',
            'Content-Type': 'application/json'
        }
        payload = {
            "model": "embedding-passage",
            "input": chunk
        }
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"[EMBED ERROR] {response.status_code} - {response.text}")
            continue

        try:
            vector = response.json()['data'][0]['embedding']
            vectors.append(vector)
        except Exception as e:
            print(f"[EMBED JSON ERROR] {e} | 응답: {response.text}")
            continue

    if not vectors:
        return []

    # 평균 벡터 계산
    mean_vector = [sum(dim) / len(vectors) for dim in zip(*vectors)]
    return mean_vector

# ===== Qdrant 처리 =====
def process_qdrant_document(user_id: str, title: str):
    source_collection = f"dream-{user_id}"
    target_collection = f"dream-{user_id}-emotion"
    print(f"🔍 분석 대상 컬렉션: {source_collection}, 타이틀: {title}")

    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # 원본 컬렉션 존재 확인
    collections = [c.name for c in client.get_collections().collections]
    if source_collection not in collections:
        print(f"❌ 컬렉션 '{source_collection}' 이 존재하지 않습니다.")
        return

    # 해당 title의 문서 조회
    scroll_result = client.scroll(
        collection_name=source_collection,
        scroll_filter=Filter(
            must=[FieldCondition(key="metadata.title", match=MatchValue(value=title))]
        ),
        with_payload=True,
        limit=1000
    )

    points = scroll_result[0]
    if not points:
        print("해당 title의 데이터가 없습니다.")
        return

    combined_text = " ".join(p.payload.get("page_content", "") for p in points)

    emotions = analyze_emotions(combined_text)
    embedding = get_mean_embedding(combined_text)

    if not embedding:
        print("❌ 임베딩 생성 실패")
        return

    # 감정 결과 저장용 컬렉션 없으면 생성
    if target_collection not in collections:
        client.recreate_collection(
            collection_name=target_collection,
            vectors_config=VectorParams(size=len(embedding), distance=Distance.COSINE)
        )
        print(f"✅ 새로운 컬렉션 생성됨: {target_collection}")

    # 포인트 생성 및 업로드
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=embedding,
        payload={
            "user_id": user_id,
            "title": title,
            "emotions": emotions,
            "full_text": combined_text
        }
    )

    client.upsert(collection_name=target_collection, points=[point])
    print(f"📌 '{target_collection}'에 감정 분석 결과 업로드 완료!")

# ===== 실행 =====
if __name__ == "__main__":
    user_id = input("사용자 ID 입력: ").strip()
    title = input("분석할 문서 title 입력: ").strip()
    process_qdrant_document(user_id, title)
