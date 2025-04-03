import os
import requests
from dotenv import load_dotenv
from agent_emotion import label_map, negative_emotions, help_resources  # 공통 상수 가져오기
import json

# 환경 변수 로드
load_dotenv()

class EmotionAgent:
    def __init__(self, emotion_scores, dream_summary=None):
        """
        :param emotion_scores: {"joy": 0.8, "sadness": 0.2, ...}
        :param dream_summary: 꿈의 핵심 내용 요약 (문자열)
        """
        if isinstance(emotion_scores, str):
            try:
                emotion_scores = json.loads(emotion_scores)
            except Exception as e:
                print(f"[EmotionAgent] JSON parsing failed: {e}")
                emotion_scores = {}

        self.emotions = [{"label": label, "score": score} for label, score in emotion_scores.items()]
        self.dream_summary = dream_summary

    def analyze_emotions_agent(self):
        # 부정 감정 점수가 높은 항목 개수 계산
        negative_count = sum(
            1 for e in self.emotions if e["label"] in negative_emotions and e["score"] > 0.3
        )

        if negative_count >= 2:
            return {"tag": "복합 부정 감정 상태", "level": "위험", "message": "두 가지 이상의 부정 감정이 강하게 감지됩니다."}
        elif any(e["label"] in negative_emotions and e["score"] > 0.5 for e in self.emotions):
            return {"tag": "부정 감정 상태", "level": "경고", "message": "부정적인 감정이 감지됩니다."}
        else:
            return {"tag": "긍정 감정 상태", "level": "안정", "message": "긍정적인 감정이 감지됩니다."}

    def create_llm_prompt(self, dream_interpretation_knowledge=""):
        """
        꿈 내용, 감정 정보, 해몽 지식을 기반으로 전문가용 프롬프트를 생성합니다.
        """

        # 감정 정보: 라벨 + 수치 리스트 (한글 변환 포함)
        emotion_lines = [
            f"- {label_map.get(e['label'], e['label'])}: {e['score']}" for e in self.emotions
        ]
        emotion_scores_text = "\n".join(emotion_lines)

        prompt = f"""
너는 꿈 분석과 심리 상담에 특화된 전문가야.

사용자가 아래의 꿈 내용을 입력했어. 너는 다음과 같은 순서로 대답해야 해:

1. 꿈의 내용을 간결하게 요약해줘.
2. 꿈의 상징과 등장 요소들을 기반으로, 미리 제공된 논문 정보와 이론에 따라 해몽해줘.
3. 감정 수치와 꿈 내용을 바탕으로 사용자의 현재 심리 상태를 분석해줘.
4. 만약 부정적인 심리 상태가 **경고 수준 이상**이라면, 따뜻하게 위로해주는 말도 함께 해줘.
5. 만약 부정적인 심리 상태가 **위험 수준**이라면, 심리 상태태를 파악하기 위한 추가 질문도 함께 포함해줘.
6. 심리 상태를 반영하는 이모티콘을 많이 사용해줘. 3문장 안에 적어도 하나의 이모티콘을 사용해서 답변해줘.

---

[꿈 내용]
{self.dream_summary.strip() if self.dream_summary else "입력된 꿈 요약 없음"}

[해몽 관련 논문 정보]
{dream_interpretation_knowledge.strip() if dream_interpretation_knowledge else "없음"}

[감정 수치]
{emotion_scores_text}

---

⛔ 절대 생략하거나 순서를 바꾸지 마.
모든 항목을 위 순서대로 반드시 포함해서 서술해줘.
친절하고 따뜻한 어조를 유지해줘.
"""
        return prompt

    def call_solar_llm(self, prompt):
        try:
            api_key = os.getenv("UPSTAGE_API_KEY")
            url = "https://api.upstage.ai/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": "solar-pro",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            # 이거 형식 맞춰 바꿔야 함
            # analysis_text = response.json()["choices"][0]["message"]["content"]
            data = response.json()
            analysis_text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if not analysis_text:
                raise ValueError("LLM 응답에 분석 내용이 없습니다.")

             # 감정 지표 딕셔너리로 변환
            emotion_dict = {
                e["label"]: e["score"]
                for e in self.emotions
            }

            return {
                "analysis-emotions": analysis_text,
                "emotions": emotion_dict
            }

        except Exception as e:
            print(f"❌ Solar API 호출 실패: {e}")
            return None
