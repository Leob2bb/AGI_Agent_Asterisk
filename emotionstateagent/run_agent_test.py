from agent.emotion_agent import EmotionAgent

def main():
    # 테스트용 감정 점수
    emotion_scores = {
        "sadness": 0.7,
        "fear": 0.6,
        "confusion": 0.3,
        "anger": 0.2,
        "caring": 0.1,
        "joy": 0.1
    }
    
    # 에이전트 생성
    agent = EmotionAgent(emotion_scores)
    
    # 사용자 텍스트
    user_text = "요즘 너무 힘들고 불안해요. 미래가 걱정돼요."
    
    # 프롬프트 생성
    prompt = agent.create_llm_prompt(user_text)
    print("생성된 프롬프트:", prompt)
    
    # LLM 호출
    response = agent.call_solar_llm(prompt)
    if response:
        print("\nLLM 응답:")
        print(response)
    
    # 감정 시각화
    agent.visualize_emotions()

if __name__ == "__main__":
    main()