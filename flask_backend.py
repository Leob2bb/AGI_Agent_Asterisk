from flask import Flask, json, jsonify, request
from flask_cors import CORS
import uuid
from datetime import datetime
from dateutil import parser
import urllib.parse
import re
# import json

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

import os
# import fitz  # PyMuPDF
from dotenv import load_dotenv
# JWT 관련 임포트 제거

# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch

# batch_parse.py 참조
from batch_parse import process_pdfs
# 감정 분석 AGENT 클래스 참조
from agent_emotion.emotion_agent import EmotionAgent
# emotion_analysis.py 참조
from emotion_analysis import process_qdrant_document, text_combining, analyze_emotions
# symbol agent 참조
from agent_symbol.symbol_agent import analyze_symbols_and_intentions


# 환경 변수 로드 (.env에 키들 있어야 함)
load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
COLLECTION_NAME = "dream-papers"

assert UPSTAGE_API_KEY, ".env에 UPSTAGE_API_KEY가 필요합니다."
assert QDRANT_URL and QDRANT_API_KEY, "Qdrant 설정이 누락되었습니다."

app = Flask(__name__)
CORS(app)

# 로깅 설정 추가
import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('dream_app.log', maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# SQLite 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dreams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# JWT 설정 제거

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# 최대 파일 크기 제한 10MB
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# JWT 관련 설정 제거

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
    dream_id = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(255))
    date = db.Column(db.String(50))
    content = db.Column(db.Text)
    file_path = db.Column(db.String(512), nullable=True)  # 텍스트 입력이면 None
    type = db.Column(db.String(10))  # 'text' or 'file'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 감정 분석 결과 넣어버리기
    emotions = db.Column(db.Text) # json 형태
    # 행동 분석 결과 넣어버리기

    def __init__(self, user_id, dream_id, title, date, content, type, emotions=None, file_path=None):
        self.id = str(uuid.uuid4())
        self.user_id = user_id
        self.dream_id = dream_id
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
    # response.headers["Connection"] = "keep-alive"
    # response.headers["Keep-Alive"] = "timeout=10, max=100"
    return "Bot is online"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    app.logger.info(f"Register request data: {data}")
    app.logger.info("회원가입 요청")

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
    
    app.logger.info(f"Login request data: {data}")
    app.logger.info("로그인 요청")

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # JWT 토큰 발급 대신 사용자 ID만 반환
        return jsonify({
            'id': user.id,
            'username': user.username,
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


def generate_dream_id(title, date):
    # 특수 문자 제거, 소문자 변환, 공백을 언더스코어로 대체
    clean_title = re.sub(r'[^\w\s]', '', title).lower().replace(' ', '_')
    
    # 날짜 형식 통일 (YYYYMMDD)
    clean_date = date.replace('-', '').replace('/', '')
    
    # 최종 dream_id 생성 (유저ID_날짜_제목)
    dream_id = f"{clean_date}_{clean_title}"
    
    # 길이 제한 (선택적)
    return dream_id[:100]

def generate_unique_dream_id(user_id, title, date):
    base_id = generate_dream_id(title, date)
    candidate_id = base_id
    suffix = 1

    while Dream.query.filter_by(user_id=user_id, dream_id=candidate_id).first():
        candidate_id = f"{base_id}_{suffix}"
        suffix += 1

    return candidate_id



@app.route('/user/<string:user_id>/dream', methods=['POST'])
# @jwt_required() 데코레이터 제거
def submit_dream_text(user_id):
    # JWT 검증 코드 제거
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'}), 400
    
    app.logger.info(f"Submit dream text request data: {data}")
    app.logger.info(f"사용자 id = {user_id}")

    # print("requests header: ", str(request.headers))

    title = data.get('title')
    date = data.get('date')
    content = data.get('content')


    if not title or not content or not date:
        return jsonify({'error': 'Title, date and content are required'}), 400

    #  2: 감정 분석을 위한 기본값을 JSON 형식으로 설정
    # 이전 코드에서는 emotions 필드가 없거나 잘못된 형식이었을 가능성 있음
    emotions = json.dumps({"emotions": []})

    # dream_id = generate_dream_id(title, date)
    dream_id = generate_unique_dream_id(user_id, title, date)

    app.logger.info(f'dream_id = {dream_id}, user_id = {user_id}')
    dream = Dream(user_id=user_id,
                  title=title,
                  date=date,
                  content=content,
                  emotions=emotions,
                  type='text',
                  dream_id=dream_id)

    db.session.add(dream)
    db.session.commit()

    #  3: 클라이언트가 기대하는 형식으로 응답 반환
    # dreamId 필드를 추가하여 프론트엔드 코드와 호환성 유지
    return jsonify({
        'id': dream.id,  # UUID 문자열
        'dreamId': dream.dream_id,
        'title': dream.title,
        'date': dream.date,
        'content': dream.content,
        'created_at': dream.created_at.isoformat()
    }), 201


@app.route('/user/<string:user_id>/dream/file', methods=['POST'])
# @jwt_required() 데코레이터 제거
def submit_dream_file(user_id):
    # JWT 검증 코드 제거

    # 요청 데이터 확인
    app.logger.info(f"Request form data: {request.form}")
    app.logger.info(f"Request files: {request.files}")

    # 필수 데이터 받기
    title = request.form.get('title')
    date = request.form.get('date')
    content = request.form.get('content', "")  # None이면 빈 문자열 처리
    # username = request.form()

    # 파일 데이터 검증
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
        
    file = request.files['file']

    # 파일 확인
    if file.filename == '':
        return jsonify({'error': 'No file uploaded'}), 400
    
    if not title or not date:
        return jsonify({'error': 'Title and date are required'}), 400

    filename = secure_filename(file.filename)
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    # 확장자 및 MIME 타입 검사
    file_ext = os.path.splitext(filename)[1].lower()
    # pdf
    if file_ext == '.pdf':
        try:
            app.logger.info('pdf 파일 처리중...')
            content = process_pdfs(UPLOAD_FOLDER, user_id, title)
        except Exception as e:
            return jsonify({'error': f'파일 처리 중 오류 발생: {str(e)}'}), 500
    
    # png, jpg (OCR 처리하는 함수 받아 처리리)
    elif file_ext in ['.png', '.jpg', '.jpeg']:
        try:
            app.logger.info('이미지 OCR 처리중... (아직 구현 안 됨)')
            pass
        except Exception as e:
            return jsonify({'error': f'이미지 처리 중 오류 발생: {str(e)}'}), 500

    else:
        app.logger.info('지원되지 않는 파일 형식입니다.')
        return jsonify({'error': '지원되지 않는 파일 형식입니다. (PDF 또는 이미지 파일만 가능)'}), 400

    # dream_id = generate_dream_id(title, date)
    dream_id = generate_unique_dream_id(user_id, title, date)


    dream = Dream(user_id=user_id, title=filename, date=date, content=content,
                  file_path=save_path, type='file', dream_id=dream_id)
    
    db.session.add(dream)
    db.session.commit()

    # 프론트엔드와 호환되는 응답 형식
    return jsonify({
        'id': dream.id,
        'dreamId': dream.dream_id,  # 프론트엔드가 기대하는 필드명
        'title': dream.title,
        'date': dream.date,
        'content': dream.content,
        'file_path': dream.file_path,
        'created_at': dream.created_at.isoformat()
    }), 201



@app.route('/user/<string:user_id>/dream/<string:dream_id>', methods=['GET'])
# @jwt_required() 데코레이터 제거
def get_dream(user_id, dream_id):

    app.logger.info(f"Get dream request - User ID: {user_id}, Dream ID: {dream_id}")
    try:
        # 먼저 UUID로 시도
        uuid_obj = uuid.UUID(dream_id)
        app.logger.info(f"Parsed UUID: {uuid_obj}")
        dream = Dream.query.filter_by(user_id=user_id, id=str(uuid_obj)).first()
    except ValueError:
        # UUID가 아니면 dream_id로 조회
        app.logger.warning("dream_id가 UUID 형식이 아님. dream_id 필드로 조회 시도.")
        dream = Dream.query.filter_by(user_id=user_id, dream_id=dream_id).first()

    
    if not dream:
        app.logger.warning(f"Dream not found for user {user_id} with ID {dream_id}")
        return jsonify({'error': 'Dream not found'}), 404
    
    #  4: 클라이언트가 기대하는 형식으로 응답 반환
    return jsonify({
        'id': dream.id,
        'dreamId': dream.dream_id,  # 프론트엔드가 기대하는 필드명
        'title': dream.title,
        'date': dream.date,
        'content': dream.content,
        'created_at': dream.created_at.isoformat(),
        'type': dream.type
    }), 200


# @app.route('/user/<string:user_id>/dreams', methods=['GET'])
# # @jwt_required() 데코레이터 제거
# def get_dreams(user_id):
#     # JWT 검증 코드 제거
    
#     dreams = Dream.query.filter_by(user_id=user_id).order_by(
#         Dream.created_at.desc()).all()
    
#     results = [{
#         'title': d.title,
#         'type': d.type,
#         'created_at': d.created_at.isoformat()
#     } for d in dreams]

#     return jsonify({'dreams': results})


@app.route('/user/<string:user_id>/dream/<string:dream_id>/analysis', methods=['GET'])
def get_dream_analysis(user_id, dream_id):
    app.logger.info(f"Get dream request - User ID: {user_id}, Dream ID: {dream_id}")
    try:
        # UUID로 먼저 시도
        uuid_obj = uuid.UUID(dream_id)
        dream = Dream.query.filter_by(user_id=user_id, id=str(uuid_obj)).first()
    except ValueError:
        # UUID가 아니면 dream_id 필드로 조회
        app.logger.warning("dream_id가 UUID 형식이 아님. dream_id 필드로 조회 시도.")
        dream = Dream.query.filter_by(user_id=user_id, dream_id=dream_id).first()

    if not dream:
        return jsonify({'error': 'Dream not found'}), 404

    
    try:
        # emotions 필드가 유효한 JSON인지 확인
        app.logger.info("emotions 필드 유효한지 확인")
        emotions_data = dream.emotions
        app.logger.info(f"emotions = {emotions_data}")

        # 문자열일 경우 JSON 파싱
        if not emotions_data:
            emotions_data = {}
        elif isinstance(emotions_data, str):
            try:
                emotions_data = json.loads(emotions_data)
            except Exception as e:
                app.logger.error(f"emotions_data JSON 파싱 실패: {e}")
                emotions_data = {}
                
        # 감정 분석
        app.logger.info("감정 분석 시작!")

        # 분석 방법 1 (심주원)
        # emotions = process_qdrant_document(user_id, title)
        # combined_text = text_combining(user_id, dream.title)
        # app.logger.info(f"combined_text length = {len(combined_text)}")
        # emotions = analyze_emotions(combined_text)
        # app.logger.info(f'심주원 emotions = {emotions}')
        
        # 분석 방법 2 (김승연)
        app.logger.info(f"감정 에이전트 class 실행")
        agent_e = EmotionAgent(emotions_data)
        prompt_e = agent_e.create_llm_prompt(dream.content)
        app.logger.info(f"감정 에이전트 실행")
        raw_analysis_emotion = agent_e.call_solar_llm(prompt_e)
        
        # 심볼 분석, 내용이 없는 경우 기본값 처리
        content = dream.content or ""
        app.logger.info(f"content = {content}")

        # "symbols", "intentions"
        formatted_response_symbol = analyze_symbols_and_intentions(content)
        app.logger.info(f"response_symbol = {formatted_response_symbol}")

        
        # "analysis-emotions", "emotions"
        # 분석 방법 1
        # formatted_analysis_emotion = {"analysis-emotions": raw_analysis_emotion.get("analysis", "분석 결과를 불러올 수 없습니다.")}
        
        # 분석 방법 2
        formatted_response_emotion = {
            "analysis-emotions": raw_analysis_emotion.get("analysis", "분석 결과를 불러올 수 없습니다."),
            "emotions": raw_analysis_emotion.get("emotions", [])
        }
        app.logger.info(f"response_emotions = {formatted_response_emotion}")

        
        # 응답 합치기
        combined_response = {**formatted_response_emotion, **formatted_response_symbol}
        # combined_response = {**formatted_analysis_emotion, **emotions, **formatted_response_symbol}     # 예상대로 잘 나오는지 확인 필요
        
        # 응답에 dream ID 정보 추가하여 프론트엔드 호환성 유지
        combined_response["dreamId"] = dream.dream_id
        combined_response["id"] = dream.id
        app.logger.info(f"combined_response = {combined_response}")
        
        return jsonify(combined_response)
    except Exception as e:
        # 오류 로깅 강화 및 상세 오류 메시지 제공
        app.logger.error(f"분석 중 오류 발생: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())   # 자세한 오류 스택 출력
        
        return jsonify({
            "error": "분석 과정에서 오류가 발생했습니다.",
            "details": str(e)
        }), 500


@app.route('/user/<string:user_id>/dream/<string:dream_id>/chat', methods=['POST'])
def process_chat_message(user_id, dream_id):
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "메시지가 제공되지 않았습니다"}), 400

    user_message = data['message']
    try:
        uuid_obj = uuid.UUID(dream_id)
        dream = Dream.query.filter_by(user_id=user_id, id=str(uuid_obj)).first()
    except ValueError:
        app.logger.warning("dream_id가 UUID 형식이 아님. dream_id 필드로 조회 시도.")
        dream = Dream.query.filter_by(user_id=user_id, dream_id=dream_id).first()

    if not dream:
        return jsonify({'error': 'Dream not found'}), 404

    
    try:
        # AI 응답 구현 (임시)
        ai_response = {
            "response": f"당신의 메시지 '{user_message}'에 대한 응답입니다. 꿈에 관한 추가 질문이 있으신가요?"
        }
        return jsonify(ai_response)
    except Exception as e:
        app.logger.error(f"채팅 처리 중 오류 발생: {str(e)}")
        return jsonify({
            "error": "채팅 처리 중 오류가 발생했습니다.",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 테이블 없으면 생성
    port = int(os.environ.get("PORT", 5000))
    app.logger.info(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)