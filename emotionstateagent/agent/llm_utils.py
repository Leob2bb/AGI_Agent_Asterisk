import os
from dotenv import load_dotenv
from openai import OpenAI  # openai==1.52.2 기준

# 환경 변수 로드
load_dotenv()

# API 키 로드
SOLAR_API_KEY = os.getenv("SOLAR_API_KEY")

# Upstage Solar API에 연결할 클라이언트 생성
client = OpenAI(
    api_key=SOLAR_API_KEY,
    base_url="https://api.upstage.ai/v1"
)

# Solar 모델 호출 함수
def generate_solar_response(system_prompt, user_prompt):
    try:
        response = client.chat.completions.create(
            model="solar-pro",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[❌ API 호출 실패] {e}")
        return "응답 생성 실패"
