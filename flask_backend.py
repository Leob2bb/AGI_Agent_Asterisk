from flask import Flask, json, jsonify, request
from flask_cors import CORS
# import uuid
from datetime import datetime
# import json

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

import os
# import fitz  # PyMuPDF
from dotenv import load_dotenv

# from langchain.schema import Document
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_upstage.embeddings import UpstageEmbeddings
# from langchain_qdrant import QdrantVectorStore
# from qdrant_client import QdrantClient
# from qdrant_client.models import Distance, VectorParams

# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

# batch_parse.py 참조
from batch_parse import process_pdfs
# 감정 분석 AGENT 클래스 참조
from agent.emotion_agent import EmotionAgent
# emotion_analysis.py 참조조
from emotion_analysis import process_qdrant_document

# 환경 변수 로드 (.env에 키들 있어야 함)
load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "dream-papers"

assert UPSTAGE_API_KEY, ".env에 UPSTAGE_API_KEY가 필요합니다."
assert QDRANT_URL and QDRANT_API_KEY, "Qdrant 설정이 누락되었습니다."

app = Flask(__name__)
CORS(app)

# SQLite 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dreams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 최대 파일 크기 제한 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# print("max_length = ", app.config.get("MAX_CONTENT_LENGTH"))


# User 모델 정의
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


# Dream 모델 정의
class Dream(db.Model):
    __tablename__ = 'dreams'
    id = db.Column(db.String(50), primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255))
    date = db.Column(db.String(50))
    content = db.Column(db.Text)
    file_path = db.Column(db.String(512), nullable=True)  # 텍스트 입력이면 None
    type = db.Column(db.String(10))  # 'text' or 'file'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 감정 분석 결과 넣어버리기
    emotions = db.Column(db.Text) # json 형태
    # 행동 분석 결과 넣어버리기

    def __init__(self, user_id, title, date, content, type, emotions, file_path=None):
        # self.dream_id = dream_id
        self.id = None  # id를 None으로 설정하면 SQLAlchemy가 자동으로 생성
        self.user_id = user_id
        self.title = title
        self.content = content
        self.date = date
        self.type = type
        self.file_path = file_path
        self.emotions = emotions


# 파일 업로드를 위한 임시 디렉토리 생성
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/')
def home():
    # print(request.headers)
    return "Bot is online"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    print("requests data: ", data)
    # print("requests header: ", str(request.headers))

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    
    user = User(username=username, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    print("requests data: ", data)
    # print("requests header: ", str(request.headers))

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({'id': user.id, 'username': user.username}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/user/<string:user_id>/dream', methods=['POST'])
def submit_dream_text(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    print("requests data: ", data)
    # print("requests header: ", str(request.headers))

    title = data.get('title')
    date = data.get('date')
    content = data.get('content')

    if not title or not content or not date:
        return jsonify({'error': 'Title, date and content are required'}), 400

    emotions = ""   # 임시

    dream = Dream(user_id=user_id,
                  title=title,
                  date=date,
                  content=content,
                  emotions=emotions,
                  type='text')

    db.session.add(dream)
    db.session.commit()

    # emotions 반영해야 함
    return jsonify({
        'title': dream.title,
        'date': dream.date,
        'content': dream.content
    }), 201


@app.route('/user/<string:user_id>/dream/file', methods=['POST'])
def submit_dream_file(user_id):
    title = request.form.get('title')  # 일반 텍스트 데이터
    date = request.form.get('date')
    content = request.form.get('content')
    file = request.files.get('file')
    print("title: ", title, "date: ", date, "content: ", content)
    print("Request files: ", request.files)

    if not title or not date or not file:
        return jsonify({'error': 'Title, date, and file are required'}), 400
    # if not content:
    #     return jsonify({'error': 'Content is required'}), 400

    # if 'file' not in request.files:
    #     return jsonify({'error': 'No file uploaded'}), 400

    if file.filename is not None:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        file_ext = os.path.splitext(filename)[1].lower()
        # 확장자가 .pdf일 경우만 실행
        if file_ext == '.pdf':
            # batch_parse.py의 함수 실행
            content = process_pdfs(UPLOAD_FOLDER, user_id, title)
            # emotion_analysis.py의 함수 실행
            emotions = process_qdrant_document(user_id, title)
            # 디버깅
            print(emotions)

    else:
        return jsonify({'error': 'Empty filename'}), 400

    dream = Dream(user_id=user_id,
                  title=filename,
                  date=date,
                  content=content,
                  file_path=save_path,
                  emotions = emotions,
                  type='file')

    db.session.add(dream)
    db.session.commit()

    # emotions 반영해야 함
    return jsonify({
        'title': dream.title,
        'date': dream.date,
        'content': dream.content,
        'file_path': dream.file_path
    }), 201


# 특정 사용자의 특정 꿈 정보를 조회하는 API
@app.route('/user/<string:user_id>/dream/<created_at>', methods=['GET'])
def get_dream(user_id, created_at):

    dream = Dream.query.filter_by(user_id=user_id, created_at=created_at).first()
    
    if dream:
        return jsonify({
            'title': dream.title,
            'date': dream.date,
            'content': dream.content,
        }), 200
    
    return jsonify({'error': 'Dream not found'}), 404


@app.route('/user/<string:user_id>/dreams', methods=['GET'])
def get_dreams(user_id):

    dreams = Dream.query.filter_by(user_id=user_id).order_by(
        Dream.created_at.desc()).all()
    
    results = [{
        'title': d.title,
        'type': d.type,
        'created_at': d.created_at.isoformat()
    } for d in dreams]

    return jsonify({'dreams': results})


@app.route('/user/<string:user_id>/dream/<created_at>/analysis', methods=['GET'])
def get_dream_analysis(user_id, created_at, content, emotions):
    # 예시 코드, 실제로는 분석 결과가 반환
    if emotions is not None:
        agent = EmotionAgent(emotions)
        prompt = agent.create_llm_prompt(content)
        # 예외 처리 필요
        analysis_result = agent.call_solar_llm(prompt)
    print("analysis_result = ", jsonify(analysis_result))
    return jsonify(analysis_result)


@app.route('/user/<user_id>/dream/<created_at>/chat', methods=['POST'])
def process_chat_message(user_id, created_at):
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "메시지가 제공되지 않았습니다"}), 400
    
    user_message = data['message']
    # ai 답변 구현
    ai_response = {
        "response": f"당신의 메시지 '{user_message}'에 대한 응답입니다. 꿈에 관한 추가 질문이 있으신가요?"
    }
    return jsonify(ai_response)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 테이블 없으면 생성
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
