import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os

# 한글 폰트 설정 (Windows 기준)
font_path = "C:/Windows/Fonts/malgun.ttf"
if os.path.exists(font_path):
    fontprop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = fontprop.get_name()
else:
    print("⚠️ Malgun Gothic 폰트를 찾을 수 없습니다.")

# 한글 라벨 매핑 딕셔너리
label_map = {
    "sadness": "슬픔",
    "fear": "두려움",
    "confusion": "혼란",
    "anger": "분노",
    "caring": "보살핌",
    "joy": "기쁨",
    "love": "사랑",
    "gratitude": "감사",
    "amusement": "재미",
    "approval": "인정",
    "admiration": "감탄",
    "neutral": "중립"
}

# 테스트용 감정 데이터
emotions = [
    {"label": "sadness", "score": 0.87},
    {"label": "fear", "score": 0.75},
    {"label": "confusion", "score": 0.62},
    {"label": "anger", "score": 0.43},
    {"label": "caring", "score": 0.21},
]

# 한글 라벨로 변환
labels = [label_map.get(e["label"], e["label"]) for e in emotions]
scores = [e["score"] for e in emotions]

# 원형 차트 그리기
plt.figure(figsize=(8, 8))
plt.pie(scores, labels=labels, autopct="%.1f%%", startangle=140)
plt.title("감정 분포", fontsize=16)
plt.axis("equal")
plt.tight_layout()
plt.show()
