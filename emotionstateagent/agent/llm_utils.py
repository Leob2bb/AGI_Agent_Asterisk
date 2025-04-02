import os
import requests
from dotenv import load_dotenv

load_dotenv()

SOLAR_API_KEY = os.getenv("SOLAR_API_KEY", "").strip()
SOLAR_API_URL = "https://api.upstage.ai/v1/chat/completions"

def generate_solar_response(system_prompt, user_prompt):
    headers = {
        "Authorization": f"Bearer {SOLAR_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "solar-1",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(SOLAR_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"[❌ Error {response.status_code}] {response.text}")
        return "응답 생성 실패"