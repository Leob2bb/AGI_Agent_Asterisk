# main.py

from agent.emotion_agent import EmotionAgent

emotion_data = {
    "joy": 0.2,
    "sadness": 0.6,
    "anger": 0.1,
    "fear": 0.1
}

user_input = "요즘 너무 피곤하고 우울해요. 매일 아침이 너무 버겁습니다."

agent = EmotionAgent(emotion_data)

print("[심리 상태 분석]")
print(agent.analyze_state())

print("\n[LLM 프롬프트]")
print(agent.generate_prompt(user_input))
