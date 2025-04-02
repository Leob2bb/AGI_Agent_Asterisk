from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import requests
import torch
import time
import json
import os

# ========== 설정 ==========
EMBEDDING_API_KEY = os.getenv("UPSTAGE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# 감정 분석 모델
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

#감정 분석 api 기본 세팅
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

#임베딩하는거거
def get_embedding(text):
    url = "https://api.upstage.ai/v1/solar/embeddings"
    headers = {
        'Authorization': f'Bearer {EMBEDDING_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "model": "embedding-passage",
        "input": text
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"[EMBED ERROR] {response.status_code} - {response.text}")
        return []

    try:
        return response.json()['data'][0]['embedding']
    except Exception as e:
        print(f"[EMBED JSON ERROR] {e} | 응답: {response.text}")
        return []

# ========== 핵심 실행 ==========
def process_qdrant_document(user_id: str, title: str):
    collection_name = f"dream-{user_id}"
    print(f"🔍 컬렉션: {collection_name}, 타이틀: {title}")

    # Qdrant 연결
    qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # collection_names 존재 확인
    collection_names = [c.name for c in qdrant_client.get_collections().collections]
    if collection_name not in collection_names:
        print(f"❌ 컬렉션 '{collection_name}' 이 존재하지 않습니다.")
        print(f"📂 현재 존재하는 컬렉션들: {collection_names}")
        return

    # title에 해당하는 모든 포인트 불러오기
    scroll_result = qdrant_client.scroll(
        collection_name=collection_name,
        scroll_filter=Filter(
            must=[
                FieldCondition(key="metadata.title", match=MatchValue(value=title))
            ]
        ),
        with_payload=True,
        limit=1000
    )

    points = scroll_result[0]
    if not points:
        print("해당 title의 데이터가 없습니다.")
        return

    # page_content 합치기
    combined_text = " ".join(p.payload.get("page_content", "") for p in points)

    # 감정 분석
    emotions = analyze_emotions(combined_text)

    # 임베딩 생성
    embedding = get_embedding(combined_text)

    # 저장
    result = {
        "title": title,
        "user_id": user_id,
        "full_text": combined_text,
        "emotions": emotions,
        "embedding": embedding
    }

    output_path = f"{title}_analyzed.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"분석 결과 저장 완료: {output_path}")
    

# ========== 예시 실행 ==========
if __name__ == "__main__":
    user_id = input("사용자 ID 입력: ").strip()
    title = input("분석할 문서 title 입력: ").strip()
    process_qdrant_document(user_id, title)
