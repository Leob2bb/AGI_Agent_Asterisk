# 🧠 **Dreaminsight**
### 당신의 꿈은 무엇을 말하고 있을까요?
#### DreamInsight는 사용자의 꿈 일기를 분석하여 심리 상태를 해석하고, 피드백을 통해 지속적으로 발전하는 꿈 해석 RAG 시스템입니다.
___
📌 주요 기능 (Features)
- ✨ 꿈 기반 심리 해석:
꿈 일기를 분석하여 감정/주제/심리적 해석 제공

- 🔍 RAG 기반 해몽 생성:
논문 기반 RAG 시스템을 통해 전문 심리 이론에 기반한 해몽 제공

- 🧾 PDF 논문 자동 임베딩 파이프라인:
논문 PDF → 텍스트 → 청크 → Qdrant 업로드 자동화

- 📈 사용자 피드백 수집:
좋아요/싫어요 클릭으로 해몽에 대한 반응 수집

- 💾 응답 버전 관리 및 저장 기능:
사용자 해몽 결과를 버전별로 기록하고 관리 가능

___
⚙️ 기술 스택 (Tech Stack)
|영역|기술|
|--|--|
|프론트엔드|React, TailwindCSS|
|백엔드|Flask, FastAPI|
|벡터 데이터베이스|Qdrant Cloud|
|임베딩|Upstage Embedding API|
|NLP| 분석	감정 분석, 주제 분석, CBT/융/프로이트 해석|
|RAG|	LangChain, QdrantVectorStore|
|기타|	SQLite (로그인 및 사용자 데이터), Kakao i Open Builder (챗봇/의도 분석)|

___
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
___
🧪 주요 기능 흐름도

사용자 꿈 입력 → 2. 감정/주제 분석

→ 3. Qdrant에서 관련 논문 검색

→ 4. RAG 기반 해석 생성

→ 5. 사용자 피드백 수집 및 저장

→ 6. 버전 관리된 결과 제공
___
Live Demo
___
Application Screens

![image](https://www.google.co.kr/url?sa=i&url=https%3A%2F%2Fwww.donga.com%2Fnews%2FCulture%2Farticle%2Fall%2F20170125%2F82580811%2F1&psig=AOvVaw3W-4aB2nX3q0brOD6nj4zc&ust=1743690601763000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCICYsOnHuYwDFQAAAAAdAAAAABAE)
___
💡 향후 계획 (Roadmap)
 - GPT와 꿈에 대한 대화형 상담 기능 추가

 - 사용자 맞춤형 해석 템플릿 생성

 - 피드백 기반 해석 자동 개선 기능
___
📬 문의
- 📧 이메일: dreaminsight@yourdomain.com

- 🧑‍💻 팀원 또는 기여자 목록은 CONTRIBUTORS.md 참고
___
⭐️ 프로젝트 목표

"심리적 통찰을 통해, 꿈을 더 깊이 이해하다."

DreamInsight는 단순한 해몽을 넘어, 개인화된 심리적 성찰의 도구가 되고자 합니다.

