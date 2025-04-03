# agent/__init__.py

# 감정 라벨 영어 → 한글 매핑
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

# 부정 감정 리스트
negative_emotions = ["sadness", "fear", "anger", "confusion"]

# 도움 받을 수 있는 리소스 (심리 상담, 자가진단 등)
help_resources = {
    "mental_health_hotline": "한국 정신건강위기상담전화 ☎️ 1577-0199",
    "cesd": "https://www.nidcd.go.kr/mhTest/suicidality2.do",
    "gad7": "https://mentalhealthscreening.org/screening-tools/anxiety"
}
