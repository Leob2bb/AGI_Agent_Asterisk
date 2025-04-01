from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import os
# import json

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# 임시 저장소 (실제 서비스에서는 데이터베이스를 사용해야 함)
# dreams_db = {}
# analysis_db = {}

app = Flask(__name__)
CORS(app)

# SQLite 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # db 파일 생성
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User 모델 정의
class User(db.Model):
    __tablename__ = 'users'  # ← 복수형으로 지정
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


# 파일 업로드를 위한 임시 디렉토리 생성
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
@app.route('/')
def home():
    return "Bot is online"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400
        
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
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
        
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({
            'message': 'Login successful',
            'userId': user.id,
            'username': user.username
        }), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# @app.route('/dreams/text', methods=['POST'])
# def submit_dreams_text():
#     # POST 요청으로 전송된 데이터 접근
#     data = request.json
#     print(data)

#     # 고유 ID 생성
#     dream_id = str(uuid.uuid4())    

#     # 데이터 저장
#     if data is not None:
#         dreams_db[dream_id] = {
#             'title': data.get('title'),
#             'date': data.get('date'),
#             'content': data.get('content'),
#             'type': 'text'
#         }
#     else:
#         return jsonify({'error': 'No data received'}), 400
    
#     # 데이터 처리...
#     return jsonify({"success": True, "received": data})


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
    with app.app_context():
        db.create_all()  # 테이블이 없으면 새로 생성됨
