import json
import requests
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키를 환경 변수에서 가져오기 (없으면 기본값 사용)
SOLAR_API_KEY = os.getenv("SOLAR_API_KEY", "up_MuJY4ZmMczx8C6XEIB7FjHHjw0qy4")

# 한글 폰트 설정 (Windows 기준)
font_path = "C:/Windows/Fonts/malgun.ttf"
if os.path.exists(font_path):
    fontprop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = fontprop.get_name()
else:
    print("⚠️ Malgun Gothic 폰트를 찾을 수 없습니다.")

# 영어 → 한글 감정 라벨 매핑
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

class EmotionAgent:
    def __init__(self, emotion_scores):
        # 감정 점수를 저장하고, 딕셔너리로 변환
        self.emotions = [{"label": label, "score": score} for label, score in emotion_scores.items()]

    def analyze_emotions(self):
        # 감정 분석 로직 (예시: 부정적인 감정이 두 가지 이상이면 위험 상태)
        negative_emotions = ["sadness", "fear", "anger", "confusion"]
        negative_count = sum(1 for e in self.emotions if e["label"] in negative_emotions and e["score"] > 0.5)

        if negative_count >= 2:
            return {"tag": "복합 부정 감정 상태", "level": "위험", "message": "두 가지 이상의 부정 감정이 강하게 감지됩니다."}
        elif any(e["label"] in negative_emotions and e["score"] > 0.5 for e in self.emotions):
            return {"tag": "부정 감정 상태", "level": "경고", "message": "부정적인 감정이 감지됩니다."}
        else:
            return {"tag": "긍정 감정 상태", "level": "안정", "message": "긍정적인 감정이 감지됩니다."}

    def create_llm_prompt(self, user_text=None):
        # 먼저 감정 분석을 수행
        emotion_analysis = self.analyze_emotions()
        
        prompt = f"""
        너는 공감 능력 높은 심리상담사입니다.  
        당신의 목표는 사용자의 감정 상태를 이해하고, 공감과 질문, 조언을 통해 안정감을 주는 것입니다.

        [감정 분석 결과]
        - 감정 상태 태그: {emotion_analysis['tag']}
        - 심각도 등급: {emotion_analysis['level']}
        - 해석: {emotion_analysis['message']}

        [감정 리스트]
        """
        for e in self.emotions:
            prompt += f"- {label_map.get(e['label'], e['label'])}: {e['score']}\n"
        
        # 사용자 입력이 있으면 추가
        if user_text:
            prompt += f"\n[사용자 메시지]\n{user_text}\n"
        
        prompt += """
        👉 아래 순서로 대화를 생성하세요:
        1. 감정에 진심으로 공감하는 말 한마디
        2. 현재 상태에 대해 더 알기 위한 짧은 질문
        3. 간단한 조언 또는 따뜻한 마무리

        4. 상담사가 전문기관 또는 도움 받을 수 있는 리소스를 안내해주세요.
        예: 한국 정신건강위기상담전화 ☎️ 1577-0199

        또한, 사용자의 상태에 따라 다음과 같은 심리 검사를 안내해줄 수 있습니다:
        - CES-D (우울증 자가진단): https://www.nidcd.go.kr/mhTest/suicidality2.do
        - GAD-7 (불안 자가진단): https://mentalhealthscreening.org/screening-tools/anxiety
        """
        return prompt

    def call_solar_llm(self, prompt):
        # Solar API 호출 함수 (API URL 및 Key 설정)
        api_url = "https://api.upstage.ai/v1/chat/completions"  # 수정된 Solar API URL
        headers = {
            "Authorization": f"Bearer {SOLAR_API_KEY}",  # 환경 변수에서 가져온 API 키 사용
            "Content-Type": "application/json"
        }
        payload = {
            "model": "solar-1",  # 사용할 모델 이름
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            print(f"API 호출 실패: {response.status_code}, {response.text}")
            return None

    def visualize_emotions(self):
        # 감정 시각화 함수
        labels = [label_map.get(e["label"], e["label"]) for e in self.emotions]
        scores = [e["score"] for e in self.emotions]

        plt.figure(figsize=(8, 8))
        plt.pie(scores, labels=labels, autopct="%.1f%%", startangle=140)
        plt.title("감정 분포", fontsize=16)
        plt.axis("equal")
        plt.tight_layout()
        plt.show()