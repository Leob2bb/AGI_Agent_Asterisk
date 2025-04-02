from agent.emotion_agent import EmotionAgent

# 감정 수치 예시
emotion_scores = [
    {"label": "sadness", "score": 0.7},
    {"label": "fear", "score": 0.5},
    {"label": "confusion", "score": 0.6},
]

# 테스트용 텍스트
user_text = "최근에 마음이 자꾸 가라앉고 감정 기복이 심해요."

# 에이전트 인스턴스 생성
agent = EmotionAgent(emotion_scores)

# 응답 생성
emotion_analysis, prompt, response = agent.generate_response(user_text)

# 출력
print("🧠 분석 중:", user_text)
print("\n🩺 심리 상태 분석 결과:")
print(emotion_analysis)
print("\n📨 LLM 프롬프트:")
print(prompt)
print("\n💬 LLM 응답:")
print(response)
