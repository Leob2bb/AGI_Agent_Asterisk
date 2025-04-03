#  **DreamInsight** 🧠

<p align="center">
  <img src="https://github.com/user-attachments/assets/31b25270-fa6f-46cd-9f75-d6dc0b8d7a08" alt="DreamInsights Banner" width="20%" />
</p>

## 📖 프로젝트 소개
### 🔍당신의 꿈은 무엇을 말하고 있을까요?
#### DreamInsight는 사용자의 꿈 일기를 분석하여 감정 및 심리 상태를 해석하고 사용자에게 피드백을 제공하는 꿈 해석 RAG 시스템입니다.

사용법
1. 회원가입을 진행한다.
2. 로그인을 한다.
3. 꿈 일기를 업로드한다(직접 입력,pdf,txt)
4. 분석 결과를 보고 챗 봇과 대화

## Application Screens
<p align="center">
  <img src="https://github.com/user-attachments/assets/4a7cf87f-6dcb-4841-9d8f-4fce25428e6e" width="450"/>
  <img src="https://github.com/user-attachments/assets/0fc7b3a8-ede7-4d77-9239-dc8868f8796f" width="530"/>
</p>

## 📌주요 기능 (Features)
- 💤 꿈 기반 심리 해석:
꿈 일기를 분석하여 감정 및 심리적 해석 제공

- 🔍 RAG 기반 해몽 생성:
논문 기반 RAG 시스템을 통해 전문 심리 이론에 기반한 해몽 제공

- 🧾 PDF 논문 자동 임베딩 파이프라인:
논문 PDF → 텍스트 → 청크 → Qdrant 업로드 자동화

- 📈 사용자 피드백 수집:
좋아요/싫어요 클릭으로 해몽에 대한 반응 수집

- 💾 응답 버전 관리 및 저장 기능:
사용자 해몽 결과를 버전별로 기록하고 관리 가능

## 🧪 주요 기능 흐름도

사용자 꿈 입력 → 2. 감정/주제 분석

→ 3. Qdrant에서 관련 논문 검색

→ 4. RAG 기반 해석 생성

→ 5. 사용자 피드백 수집 및 저장

→ 6. 버전 관리된 결과 제공
```
dreaminsight/
├── frontend/               # React 기반 UI
├── backend/                # Flask API 서버
│   ├── rag/                # RAG 파이프라인
│   ├── feedback/           # 피드백 저장 및 버전 관리
│   ├── embedding/          # PDF 임베딩 파이프라인
├── data/
│   └── papers/             # 업로드한 논문 PDF
├── qdrant/                 # Qdrant 연동 스크립트
├── README.md
```
## ⚙️ 기술 스택 (Tech Stack)
|영역|기술|
|--|--|
|프론트엔드|React|
|백엔드|Flask|
|벡터 데이터베이스|Qdrant Cloud|
|임베딩|Upstage Embedding API|
|RAG|	LangChain, QdrantVectorStore|
|기타|	SQLite (로그인 및 사용자 데이터),documnet parse, LLM|

## Live Demo

## 💡향후 계획 (Roadmap)
 - GPT와 꿈에 대한 대화형 상담 기능 추가

 - 사용자 맞춤형 해석 템플릿 생성

 - 피드백 기반 해석 자동 개선 기능
 - 꿈 커뮤니티를 개설

## 📬 문의
- 📧 이메일: dreaminsight@yourdomain.com

- 🧑‍💻 팀원 또는 기여자 목록은 CONTRIBUTORS.md 참고
