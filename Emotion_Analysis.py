import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# 모델 준비 (멀티라벨 감정 분류 모델)
model_name = "j-hartmann/emotion-english-distilroberta-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 감정 라벨 정의
emotion_labels = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
                  'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
                  'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
                  'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
                  'relief', 'remorse', 'sadness', 'surprise', 'neutral']

# 분석 함수
def analyze_emotions(text, threshold=0.3):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    probs = torch.sigmoid(logits).squeeze().tolist()

    # 점수 기준으로 필터링 및 정렬
    results = [
        {"label": label, "score": round(score, 3)}
        for label, score in zip(emotion_labels, probs)
        if score > threshold
    ]
    return sorted(results, key=lambda x: x["score"], reverse=True)

# 꿈 데이터 로드
with open("reddit_dreams.json", "r", encoding="utf-8") as f:
    dreams = json.load(f)

analyzed = []

for d in dreams:
    content = d.get("content", "").strip()
    title = d.get("title", "").strip()

    if not content:
        emotions = []
    else:
        try:
            emotions = analyze_emotions(content)
        except Exception as e:
            print(f"[ERROR] {title}: {e}")
            emotions = []

    analyzed.append({
        "title": title,
        "content": content,
        "emotions": emotions  # 멀티 감정 배열로 저장
    })

# 결과 저장
with open("dreams_with_emotions.json", "w", encoding="utf-8") as f:
    json.dump(analyzed, f, indent=2, ensure_ascii=False)
