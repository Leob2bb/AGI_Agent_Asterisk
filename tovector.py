import requests
import json

API_KEY = "up_ksfeJdqOSHRxTrTFk4tO2hCxyGzfv"

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
EMBEDDING_URL = 'https://api.upstage.ai/v1/solar/embeddings'

def get_embedding(text):
    payload = {
        "model": "embedding-passage",
        "input": text
    }
    response = requests.post(EMBEDDING_URL, headers=HEADERS, json=payload)
    return response.json()['data'][0]['embedding']

# 파일에서 꿈 일기 로드
with open("reddit_dreams.json", "r", encoding="utf-8") as f:
    dreams = json.load(f)

docs = [d['content'] for d in dreams if d['content'].strip()]

# 임베딩 추출
embeddings = [get_embedding(doc) for doc in docs]
