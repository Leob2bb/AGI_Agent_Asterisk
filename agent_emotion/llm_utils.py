import os
import requests
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# API 키 로드
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
SOLAR_API_KEY = UPSTAGE_API_KEY

SOLAR_API_URL = "https://api.upstage.ai/v1/chat/completions"

def generate_solar_response(system_prompt, user_prompt):
    headers = {
        "Authorization": f"Bearer {SOLAR_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "solar-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(SOLAR_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[❌ API 호출 실패] {e}")
        return "응답 생성 실패"


def call_solar_chat(messages):
        url =  "https://api.upstage.ai/v1/chat/completions" # 실제 API URL
        token = UPSTAGE_API_KEY
        payload = {
            "model": "solar-pro",
            "messages": messages,
            "temperature": 0.7
        }

        headers = {
            "Authorization": f"Bearer {UPSTAGE_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.post(UPSTAGE_API_KEY, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]