import os
import requests
from dotenv import load_dotenv
import json

# .env 로드
load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYMBOL_PATH = os.path.join(BASE_DIR, "dream_symbols.json")

with open(SYMBOL_PATH, "r", encoding="utf-8") as f:
    SYMBOL_ENTRIES = json.load(f)

def extract_symbols(text):
    found = []
    text_lower = text.lower()
    for entry in SYMBOL_ENTRIES:
        for keyword in entry["keywords"]:
            if keyword.lower() in text_lower:
                found.append({
                    "object": entry["object"],
                    "matched": keyword,
                    "meanings": entry["meanings"]
                })
                break
    return found

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
            llm_response = response.json()['choices'][0]['message']['content']
            print("[LLM DEBUG 응답]", llm_response)
            parsed = json.loads(llm_response)

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
            print(f"[LLM ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[LLM PARSE ERROR] {e}")
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
            llm_response = response.json()['choices'][0]['message']['content']
            print("[LLM DEBUG 응답]", llm_response)
            parsed = json.loads(llm_response)

            if isinstance(parsed, dict):
                for val in parsed.values():
                    if isinstance(val, list) and all(isinstance(item, dict) and ("object" in item or "action" in item) for item in val):
                        parsed = val
                        break

            if isinstance(parsed, list) and all(isinstance(item, dict) and ("object" in item or "action" in item) for item in parsed):
                return parsed
            else:
                print("[WARNING] LLM 응답 형식이 예상과 다름. 생략 처리.")
                return []
        else:
            print(f"[LLM ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[LLM PARSE ERROR] {e}")
    return []

def analyze_symbols_and_intentions(text):
    symbols = extract_symbols(text)

    if len(symbols) < 2:
        print("🤖 LLM 상징 해석 보완 수행")
        llm_symbols = llm_symbolic_supplement(text)
        existing = {s['object'] for s in symbols if "object" in s}
        symbols += [s for s in llm_symbols if s.get("object") not in existing]
    else:
        print("✅ 규칙 기반 상징 해석으로 충분")

    intentions = llm_intention_supplement(text)

    return {
        "symbols": symbols,
        "intentions": intentions
    }