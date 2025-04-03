import requests
import os
from dotenv import load_dotenv
import json

import base64
import json
from openai import OpenAI

load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

 # ------------------------------------
# Document OCR
# filename = "YOUR_FILE_NAME"
 
# url = "https://api.upstage.ai/v1/document-digitization"
# headers = {"Authorization": f"Bearer {UPSTAGE_API_KEY}"}
 
# files = {"document": open(filename, "rb")}
# data = {"model": "ocr"}
# response = requests.post(url, headers=headers, files=files, data=data)
 
# print(response.json())


 # ------------------------------------
# Informnation Extraction (Auto Schema generation)
 
client = OpenAI(
    api_key=UPSTAGE_API_KEY,
    base_url="https://api.upstage.ai/v1"
)
 
# base64로 인코딩
def encode_img_to_base64(img_path):
    with open(img_path, 'rb') as img_file:
        img_bytes = img_file.read()
        base64_data = base64.b64encode(img_bytes).decode('utf-8')
        return base64_data
 
# Schema generation request
def schema_generation_auto(img_path):
    url = "https://api.upstage.ai/v1/information-extraction"
    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    base64_data = encode_img_to_base64(img_path)
    mime_type = "image/jpeg" if img_path.lower().endswith((".jpg", ".jpeg")) else "image/png"

    data = {
        "model": "information-extract",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_data}"
                        }
                    }
                ]
            }
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "dream_diary_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {
                        "type": "string",
                        "description": "꿈의 제목"
                        },
                        "date": {
                            "type": "string",
                            "description": "꿈을 꾼 날짜 (예: 2024-03-10)"
                        },
                        "emotion": {
                            "type": "string",
                            "description": "꿈을 통해 느낀 주요 감정 (예: 공포, 기쁨, 혼란 등)"
                        },
                        "characters": {
                            "type": "array",
                            "description": "꿈에 등장한 인물 목록",
                            "items": {"type": "string"}
                        },
                        "actions": {
                            "type": "array",
                            "description": "꿈 속에서 벌어진 주요 행동",
                            "items": {"type": "string"}
                        },
                        "backgrounds": {
                            "type": "array",
                            "description": "꿈에서 배경이 된 장소나 환경 (예: 학교, 숲, 불타는 건물 등)",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["title", "date", "emotion", "characters", "actions", "backgrounds"]
                }
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        result = response.json()
        if response.status_code == 200:
            print(json.dumps(result, indent=4, ensure_ascii=False))
        else:
            print(f"❌ 오류 발생 (status code {response.status_code})")
            print(json.dumps(result, indent=4, ensure_ascii=False))
    except Exception as e:
        print("❌ JSON 디코딩 실패:", e)
        print("응답 원문:", response.text)



    

# Use clear key names and descriptions: Providing clear and descriptive key names and descriptions significantly improves the accuracy of data extraction.
# Avoid vauge or overly generic key names: Use specific terms where applicable, and include concise descriptions that explain the purpose and expected values of each key.

# ------------------------------------
# 자동 schema를 사용해 IE
# Information Extraction Request using the generated schema
def information_extraction(base64_data):
    extraction_response = client.chat.completions.create(
        model="information-extract",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url":{
                            "url": f"data:image/png;base64,{base64_data}"
                            }
                    }
                ]
            }
        ],
        response = client.chat.completions.create(
    model="information-extract",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_data}"
                    }
                }
            ]
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "dream_diary_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "꿈의 제목"
                    },
                    "date": {
                        "type": "string",
                        "description": "꿈을 꾼 날짜"
                    },
                    "emotion": {
                        "type": "string",
                        "description": "꿈에서 느낀 감정"
                    },
                    "characters": {
                        "type": "array",
                        "description": "등장 인물",
                        "items": { "type": "string" }
                    },
                    "actions": {
                        "type": "array",
                        "description": "주요 행동",
                        "items": { "type": "string" }
                    },
                    "backgrounds": {
                        "type": "array",
                        "description": "꿈의 배경/장소",
                        "items": { "type": "string" }
                    }
                },
                "required": ["title", "date", "emotion", "characters", "actions", "backgrounds"]
            }
        }
    }
)


)
    

    print(extraction_response.choices[0].message.content)

if __name__ == "__main__":
    img_path = "D:/agi_asterisk_master/grimdiary.jpg"

    if not img_path.lower().endswith((".png", ".jpg", ".jpeg")):
        print("⚠️ Error: PNG 또는 JPG 이미지로 변환하세요.")
    elif not os.path.exists(img_path):
        print("❌ 파일이 존재하지 않습니다:", img_path)
    else:
        schema_generation_auto(img_path)
