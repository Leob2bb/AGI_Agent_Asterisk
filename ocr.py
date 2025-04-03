import requests
import os
from dotenv import load_dotenv

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
def schema_generation_auto(base64_data):
    schema_response = client.chat.completions.create(
        model="information-extract",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{base64_data}"
                    }
                ]
            }
        ],
    )

    # 자동 생성된 schema -> 보고 수정 필요
    try:
        schema = json.loads(schema_response.choices[0].message.content)
        print(json.dumps(schema, indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Error: API 응답을 JSON으로 변환할 수 없습니다.")
        print("응답 내용:", schema_response.choices[0].message.content)
    

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
                        "image_url": f"data:image/png;base64,{base64_data}"
                    }
                ]
            }
        ],
        response_format="json"
    )

    print(extraction_response.choices[0].message.content)

if __name__ == "__main__":
    # img_path = "D:/Yonsei_2025/Side_Project/agi_agent_hackathon_3/diary_template/diary_pink.pdf"
    img_path = "D:/Yonsei_2025/Side_Project/agi_agent_hackathon_3/diary_template/Diary1.png"

    # 🔥 FIXED: PDF 파일이 이미지가 아니라서 API가 지원하지 않을 가능성 높음 -> PNG 등으로 변환 필요
    if not img_path.lower().endswith((".png", ".jpg", ".jpeg")):
        
        print("⚠️ Error: 지원되지 않는 파일 형식입니다. PNG 또는 JPG 이미지로 변환하세요.")
    else:
        base64_data = encode_img_to_base64(img_path)
        schema_generation_auto(base64_data)