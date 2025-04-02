from agent.emotion_agent import EmotionAgent

emotions = {
    "sadness": 0.7,
    "joy": 0.2,
    "anger": 0.65
}

user_text = "요즘 무기력하고 화가 나요. 아무것도 하기 싫어요."

agent = EmotionAgent(emotions)
prompt = agent.create_llm_prompt(user_text)
print("📝 생성된 프롬프트:\n", prompt)

response = agent.call_solar_llm(prompt)
print("\n💬 LLM 응답:\n", response)

agent.visualize_emotions()
