
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

# 상징 추출 (symbol_dict 기반)
def extract_symbols(text):
    return [
        {"object": keyword, "meaning": meaning}
        for keyword, meaning in symbol_dict.items()
        if keyword in text
    ]

# LLM를 이용한 의도 해석
def llm_intention_supplement(text):
    url = "https://api.upstage.ai/v1/solar/chat/completions"
    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-pro-1-chat",
        "messages": [
            {
                "role": "system",
                "content": "당신은 꿈 해석 전문가입니다. 사용자의 꿈 내용을 바탕으로 꿈 속 행동이나 상황이 나타내는 심리적 의도 또는 무의식을 추론해주세요."
            },
            {
                "role": "user",
                "content": f"""
다음은 꿈 내용입니다. 이 꿈에서 사용자의 **의도**, **심리적 상태**, **무의식의 목적**을 해석해주세요.

{text}

결과는 한국어로 JSON 배열 형태로 반환해주세요.
예시:
[
  "심리적 불안정과 통제력 상실",
  "외부 자극 회피",
  "감정 해소 욕구"
]
"""
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            gpt_response = response.json()['choices'][0]['message']['content']
            return json.loads(gpt_response)
        else:
            print(f"[GPT ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[GPT PARSE ERROR] {e}")
    return ["명확한 의도 분석 불가"]

# LLM 기반 상징 해석 (보완용)
def llm_symbolic_supplement(text):
    url = "https://api.upstage.ai/v1/solar/chat/completions"
    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-pro-1-chat",
        "messages": [
            {
                "role": "system",
                "content": "당신은 꿈 해석 전문가입니다. 꿈 내용을 심리학적으로 상징 분석 해주세요."
            },
            {
                "role": "user",
                "content": f"""
다음 꿈 내용에서 상징적인 사물, 행동, 인물 등을 찾아 심리적 의미로 해석해주세요.

{text}

반드시 JSON 배열 형태로 반환해주세요.
예시:
[
  {{ "object": "물", "meaning": "감정, 무의식" }},
  {{ "object": "절벽", "meaning": "위기의 순간, 중요한 선택" }}
]
"""
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            gpt_response = response.json()['choices'][0]['message']['content']
            return json.loads(gpt_response)
        else:
            print(f"[GPT ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[GPT PARSE ERROR] {e}")
    return []

# 메인 함수
def analyze_symbols_and_intentions(text):
    symbols = extract_symbols(text)

    # 상징이 너무 적을 때만 llm으으로 보완
    if len(symbols) < 2:
        print("🤖 GPT 상징 해석 보완 수행")
        gpt_symbols = llm_symbolic_supplement(text)
        existing = {s['object'] for s in symbols}
        symbols += [s for s in gpt_symbols if s['object'] not in existing]
    else:
        print("✅ 규칙 기반 상징 해석으로 충분")

    # 의도는 항상 GPT로 수행
    intentions = llm_intention_supplement(text)

    return {
        "symbols": symbols,
        "intentions": intentions
    }
