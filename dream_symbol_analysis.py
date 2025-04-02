import os
import requests
from dotenv import load_dotenv
import json

# .env 로드
load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")

# 확장된 상징 사전
symbol_dict = {
    "물": "감정, 무의식",
    "바다": "광대한 감정, 무의식",
    "불": "파괴, 정화, 열정",
    "산": "도전, 극복, 자기 성장",
    "절벽": "위기, 선택의 갈림길",
    "하늘": "정신적 확장, 희망",
    "어둠": "불안, 미지, 감정 억눌림",
    "빛": "희망, 진실, 자각",
    "고래": "깊은 감정, 무의식과의 연결",
    "뱀": "불안, 변화, 치유",
    "호랑이": "힘, 공격성, 본능",
    "늑대": "고독, 직관, 본능적 욕구",
    "새": "자유, 정신적 상승",
    "거미": "복잡한 감정, 통제 욕구",
    "나무": "생명력, 자기 성장",
    "비": "감정 정화, 슬픔, 변화",
    "떨어짐": "불안, 실패, 통제력 상실",
    "비행": "자유, 도피, 해방",
    "도망": "문제 회피, 스트레스",
    "죽음": "종결, 변화, 새로운 시작",
    "아이": "순수성, 보호 본능",
    "학교": "학습, 평가, 과거의 압박",
    "병원": "치유, 회복, 불안감",
    "집": "자기 정체성, 내면세계",
    "길": "인생의 방향, 선택",
    "엄마": "보호, 의존, 감정 연결",
    "아버지": "권위, 보호자, 도전",
    "연인": "애착, 욕망, 관계 갈등",
    "죽은 사람": "미련, 회한, 과거와의 연결"
}

def extract_symbols(text):
    return [
        {"object": keyword, "meaning": meaning}
        for keyword, meaning in symbol_dict.items()
        if keyword in text
    ]

def llm_intention_supplement(text):
    url = "https://api.upstage.ai/v1/solar/chat/completions"
    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-pro",
        "top_p": 1,
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": "당신은 꿈 해석 전문가이며, 무의식, 감정 상태, 내면의 심리를 추론하는 역할을 합니다."
            },
            {
                "role": "user",
                "content": f"""
다음 꿈의 내용에서 사용자의 무의식적 의도, 감정 상태, 심리적 동기를 분석해주세요.

반드시 JSON 배열 형태로 분석 결과를 반환해주세요.
형식 예시:
[
  "불안정한 감정 상태에서 도망치고자 하는 심리",
  "무의식적인 감정 정화 욕구",
  "자기 통제력 상실에 대한 불안"
]

꿈 내용:
{text}
"""
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            gpt_response = response.json()['choices'][0]['message']['content']
            print("[GPT DEBUG 응답]", gpt_response)
            parsed = json.loads(gpt_response)

            if isinstance(parsed, dict):
                merged = []
                for v in parsed.values():
                    if isinstance(v, list):
                        merged.extend(v)
                    elif isinstance(v, str):
                        merged.append(v)
                return merged
            elif isinstance(parsed, list):
                return parsed
        else:
            print(f"[GPT ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[GPT PARSE ERROR] {e}")
    return ["명확한 의도 분석 불가"]

def llm_symbolic_supplement(text):
    url = "https://api.upstage.ai/v1/solar/chat/completions"
    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-pro",
        "top_p": 1,
        "temperature": 0.7,
        "messages": [
            {
                "role": "system",
                "content": "당신은 꿈 분석 전문가이며, 상징과 심리적 의미를 구조화된 JSON 형식으로 분석하는 역할을 합니다."
            },
            {
                "role": "user",
                "content": f"""
다음 꿈 내용에서 등장하는 사물, 인물, 행동, 장소 등을 분석하여
각 요소가 나타내는 심리적/무의식적 의미를 해석해주세요.

반드시 아래와 같은 JSON 배열 형식으로 반환해주세요.
[
  {{ "object": "물", "meaning": "감정, 무의식과 관련된 상징" }},
  {{ "object": "불", "meaning": "감정 폭발, 정화 또는 파괴의 의미" }}
]

꿈 내용:
{text}
"""
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            gpt_response = response.json()['choices'][0]['message']['content']
            print("[GPT DEBUG 응답]", gpt_response)
            parsed = json.loads(gpt_response)

            if isinstance(parsed, dict):
                for val in parsed.values():
                    if isinstance(val, list) and all(isinstance(item, dict) and ("object" in item or "action" in item) for item in val):
                        parsed = val
                        break

            if isinstance(parsed, list) and all(isinstance(item, dict) and ("object" in item or "action" in item) for item in parsed):
                return parsed
            else:
                print("[WARNING] GPT 응답 형식이 예상과 다름. 생략 처리.")
                return []
        else:
            print(f"[GPT ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[GPT PARSE ERROR] {e}")
    return []

def analyze_symbols_and_intentions(text):
    symbols = extract_symbols(text)

    if len(symbols) < 2:
        print("🤖 GPT 상징 해석 보완 수행")
        gpt_symbols = llm_symbolic_supplement(text)
        existing = {s['object'] for s in symbols if "object" in s}
        symbols += [s for s in gpt_symbols if s.get("object") not in existing]
    else:
        print("✅ 규칙 기반 상징 해석으로 충분")

    intentions = llm_intention_supplement(text)

    return {
        "symbols": symbols,
        "intentions": intentions
    }