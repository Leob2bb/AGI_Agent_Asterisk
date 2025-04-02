
import os
import requests
from dotenv import load_dotenv

# .env 로드
load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")

# ✅ 상징 사전
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
    "새": "자유, 정신적 상승",
    "거미": "복잡한 감정, 통제 욕구",
    "나무": "생명력, 자기 성장",
    "떨어짐": "불안, 실패, 통제력 상실",
    "비행": "자유, 도피, 해방",
    "도망": "문제 회피, 스트레스",
    "죽음": "종결, 변화, 새로운 시작",
    "아이": "순수성, 보호 본능",
    "학교": "학습, 평가, 과거의 압박",
    "집": "자기 정체성, 내면세계",
    "병원": "치유, 회복, 불안감",
    "길": "인생의 방향, 선택",
    "엄마": "보호, 의존, 감정 연결",
    "죽은 사람": "미련, 회한, 과거와의 연결",
    "연인": "애착, 욕망, 관계 갈등"
}

# ✅ 의도 추론 규칙
intention_rules = [
    ("떨어지다", "심리적 불안정, 실패에 대한 두려움"),
    ("도망치다", "문제를 회피하려는 심리"),
    ("숨다", "불안 회피, 외부 자극 차단 욕구"),
    ("울다", "감정의 해소, 내면 슬픔 표현"),
    ("죽다", "자아의 변화, 새로운 시작에 대한 두려움"),
    ("불나다", "강렬한 감정 폭발 또는 파괴 욕구"),
    ("연인", "관계 욕구, 소속감 또는 이별 불안"),
    ("학교", "자기 평가, 과거 스트레스"),
    ("아이", "보호받고 싶은 욕망, 순수함"),
    ("비행", "현실 회피, 해방 욕구")
]

def extract_symbols(text):
    found_symbols = []
    for keyword, meaning in symbol_dict.items():
        if keyword in text:
            found_symbols.append({"object": keyword, "meaning": meaning})
    return found_symbols

def infer_intentions(text):
    inferred = []
    for keyword, meaning in intention_rules:
        if keyword in text:
            inferred.append(meaning)
    return list(set(inferred)) or ["명확한 의도 분석 불가"]

def gpt_symbolic_supplement(text):
    url = "https://api.upstage.ai/v1/solar/chat/completions"
    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "solar-pro-1-chat",
        "messages": [
            {"role": "system", "content": "당신은 꿈 분석 전문가입니다. 사용자의 꿈 내용을 기반으로 상징적 의미를 심리학적으로 추론해 주세요."},
            {"role": "user", "content": f"""
다음 꿈 내용을 상징적으로 해석해주세요.

{text}

각 사물, 행동, 등장인물 등이 어떤 심리적/상징적 의미를 갖는지 분석해 주세요.
결과는 반드시 JSON 배열로 출력해주세요. 형식 예:
[
  {{ "object": "고래", "meaning": "무의식과의 연결" }},
  {{ "object": "물", "meaning": "감정, 무의식" }}
]
"""}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            gpt_response = response.json()['choices'][0]['message']['content']
            import json
            return json.loads(gpt_response)
        else:
            print(f"[GPT ERROR] {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[GPT PARSE ERROR] {e}")
    return []

def analyze_symbols_and_intentions(text):
    rules_result = {
        "symbols": extract_symbols(text),
        "intentions": infer_intentions(text)
    }

    should_use_gpt = (
        len(rules_result["symbols"]) < 2 or
        rules_result["intentions"] == ["명확한 의도 분석 불가"]
    )

    if should_use_gpt:
        print("🤖 GPT 보완 해석 활성화됨 (규칙 기반 결과 부족)")
        gpt_symbols = gpt_symbolic_supplement(text)
        existing_objects = {s["object"] for s in rules_result["symbols"]}
        new_symbols = [s for s in gpt_symbols if s["object"] not in existing_objects]
        rules_result["symbols"].extend(new_symbols)
    else:
        print("✅ 규칙 기반 해석으로 충분하여 GPT 호출 생략")

    return rules_result
