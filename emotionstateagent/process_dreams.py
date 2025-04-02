import json
from agent.emotion_agent import EmotionAgent

# 1. 파일 경로
INPUT_PATH = "dreams_with_emotions.json"
OUTPUT_PATH = "dreams_with_responses.json"

# 2. JSON 파일 로딩
with open(INPUT_PATH, "r", encoding="utf-8") as f:
    dreams = json.load(f)

results = []

# 3. 꿈 데이터 반복 처리
for dream in dreams:
    title = dream.get("title", "")
    content = dream.get("content", "")
    emotions_raw = dream.get("emotions", [])

    # 감정 배열을 dict로 변환
    emotion_scores = {e["label"]: e["score"] for e in emotions_raw}

    # 에이전트 분석 실행
    agent = EmotionAgent(emotion_scores)

    try:
        state = agent.analyze_state()
        response = agent.call_llm(content)

    except Exception as e:
        state = {"tag": "에러", "level": "에러", "message": str(e)}
        response = "[ERROR] LLM 응답 생성 실패"

    # 결과 추가
    dream_result = {
        "title": title,
        "content": content,
        "emotions": emotions_raw,
        "state": state,
        "llm_response": response
    }
    results.append(dream_result)

# 4. 출력 저장
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"[완료] 분석 결과 저장: {OUTPUT_PATH}")
