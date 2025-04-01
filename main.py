from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import os
import json


# 임시 저장소 (실제 서비스에서는 데이터베이스를 사용해야 함)
dreams_db = {}
analysis_db = {}

app = Flask(__name__)
# 모든 출처 허용 또는 React 앱의 Replit URL만 허용
CORS(app)

# 파일 업로드를 위한 임시 디렉토리 생성
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
@app.route('/')
def home():
    return "Bot is online"

@app.route('/dreams/text', methods=['POST'])
def submit_dreams_text():
    # POST 요청으로 전송된 데이터 접근
    data = request.json
    print(data)

    # 고유 ID 생성
    dream_id = str(uuid.uuid4())

    # 데이터 저장
    if data is not None:
        dreams_db[dream_id] = {
            'title': data.get('title'),
            'date': data.get('date'),
            'content': data.get('content'),
            'type': 'text'
        }
    else:
        return jsonify({'error': 'No data received'}), 400
    
    # 데이터 처리...
    return jsonify({"success": True, "received": data})


# @app.route('/dreams/file', methods=['POST'])
# def register_dream_file():
#     # 파일 업로드를 위한 꿈 정보 등록
#     data = request.json

#     # 고유 ID 생성
#     dream_id = str(uuid.uuid4())

#     # 데이터 저장
#     dreams_db[dream_id] = {
#         'title': data.get('title'),
#         'date': data.get('date'),
#         'content': None,  # 파일 업로드 후 내용이 채워질 예정
#         'type': 'file',
#         'file_path': None  # 파일 업로드 후 경로가 채워질 예정
#     }

#     return jsonify({"success": True, "id": dream_id})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)