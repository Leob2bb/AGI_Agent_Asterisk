#  **DreamInsight** 🧠

<p align="center">
  <img src="https://github.com/user-attachments/assets/31b25270-fa6f-46cd-9f75-d6dc0b8d7a08" alt="DreamInsights Banner" width="20%" />
</p>

## 📖 프로젝트 소개
### 🔍당신의 꿈은 무엇을 말하고 있을까요?
#### DreamInsight는 사용자의 꿈 일기를 분석하여 심리 상태를 해석하고 사용자에게 피드백을 제공하는 꿈 해석 시스템입니다.

## 📌DreamInsigh 주요 기능
### 🔑로그인
- 회원가입 후 로그인을 진행한다.
<p align="center">
  <img src="https://github.com/user-attachments/assets/4a7cf87f-6dcb-4841-9d8f-4fce25428e6e" width="280"/>
  <img src="https://github.com/user-attachments/assets/0fc7b3a8-ede7-4d77-9239-dc8868f8796f" width="330"/>
</p>

### 꿈 데이터 입력 시스템
- 꿈 일기를 업로드한다.(파일/텍스트 업로드 가능)

- 꿈 기록 열람 및 관리

### 개인화된 심리 분석 및 피드백 제공
- 심리 상태 자동으로 분석

### 히스토리 기반 상호작용
- 분석 결과를 보고 챗 봇과 대화

## 🪛DreamInsigh 주요 특징 

- 🔍 RAG 기반 꿈 해석 시스템 구축
사용자의 꿈 데이터를 기반으로 Qdrant에서 관련 논문 정보를 검색하고, 이를 LLM에 전달하여 심리학 이론 기반 해석을 생성합니다.
→ Retrieval-Augmented Generation 구조

- 📄 PDF 꿈 일기 자동 임베딩 파이프라인
사용자가 업로드한 꿈 일기 PDF를 텍스트로 변환한 후, 문단 단위 청크로 나누고 Upstage 임베딩 API로 벡터화하여 Qdrant에 자동 업로드
→ PDF → 텍스트 → 청크 → 벡터 → Qdrant

- 💬 감정 분석 및 상징/의도 추출 API 연동
감정 분석 API를 통해 꿈의 정서적 흐름을 파악하고, 상징 해석 API로 무의식적 메시지와 상징을 분석
→ 감정 태깅 + 상징 키워드 추출 → 해석 근거로 사용

- 🤖 Solar Pro LLM 기반 해석 생성 모듈
사용자 감정 + 상징 정보 + 관련 논문 벡터들을 LLM에 전달하여, 심리학 이론(CBT, 프로이트, 융 등)에 기반한 맞춤형 해몽을 자동 생성

- 💾 Qdrant 기반 벡터 저장소 관리 및 메타데이터 활용
저장된 논문 및 꿈 일기 벡터는 title, source, chunk_id 등의 메타데이터를 기반으로 그룹화 및 후처리 가능
→ 감정 분석, 요약, 비교 분석 등에 활용

- 🗂 꿈 해석 히스토리 DB 및 응답 버전 관리
생성된 해석은 사용자별 DB에 저장되며, 각 버전에 대한 피드백(좋아요/싫어요)과 질문 응답을 통해 해석이 지속적으로 개선됨

- 👍 사용자 피드백 수집 시스템
웹 UI 상에서 사용자 클릭으로 긍정/부정 피드백 수집 → DB 연동 → 해석 개선에 활용
→ "좋아요/싫어요", 추가 질문 기능 연동
## 🧪 DreamInsigh 솔루션 구조

1. 사용자 꿈 입력

2. 데이터 저장 및 전처리 (백엔드)

3. 감정/의도 분석 및 벡터 저장

4. 해석 생성 (LLM 연동)

5. 응답 저장 및 질의응답 반복
```
dreaminsight/
├── frontend/         # React 기반 사용자 인터페이스
├── backend/          # Flask 백엔드 서버
│   └── SQLite        # 사용자 정보 및 꿈 일기 저장
├── analysis/
│   ├── emotion/      # 감정 분석 API 연동
│   └── symbol/       # 상징 및 의도 분석 모듈
├── embedding/
│   └── qdrant/       # 벡터 저장 및 논문 연동
├── llm/
│   └── interpret/    # Solar Pro LLM 연동하여 해석 생성
├── feedback/         # 사용자 피드백 저장 및 대화 관리
```
## ⚙️ 기술 스택 (Tech Stack)
|영역|기술|
|--|--|
|프론트엔드|React|
|백엔드|Flask|
|벡터 데이터베이스|QdrantVectorStore|
|임베딩|Upstage Embedding API|
|RAG|LangChain|
|기타|SQLite, Documnet Parse, Solar Pro LLM)|

## Live Demo

## 💡향후 계획 (Roadmap)
 - GPT와 꿈에 대한 대화형 상담 기능 추가

 - 사용자 맞춤형 해석 템플릿 생성

 - 피드백 기반 해석 자동 개선 기능
   
 - 꿈 커뮤니티를 개설

## 📬 문의
- 📧 이메일: dreaminsight@yourdomain.com

- 🧑‍💻 팀원 또는 기여자 목록은 CONTRIBUTORS.md 참고
