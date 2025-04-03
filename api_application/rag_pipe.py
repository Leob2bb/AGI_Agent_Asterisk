import os
import json
from dotenv import load_dotenv

from langchain_upstage.embeddings import UpstageEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_core.runnables import RunnableMap

# 1. 환경 변수 로드
load_dotenv()

UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

assert UPSTAGE_API_KEY, ".env에 UPSTAGE_API_KEY가 필요합니다."
assert QDRANT_URL and QDRANT_API_KEY, "Qdrant 설정이 누락되었습니다."

# 2. Qdrant 연결 + 임베딩 모델
embedding_model = UpstageEmbeddings(api_key=UPSTAGE_API_KEY, model="embedding-passage")
qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name="dream-papers",
    embedding=embedding_model,
)

# 3. LLM 설정 (Upstage via OpenAI-compatible API)
llm = ChatOpenAI(
    openai_api_key=UPSTAGE_API_KEY,
    openai_api_base="https://api.upstage.ai/v1",
    model_name="solar-pro"
)

# 4. 사용자 꿈 일기 불러오기
with open("dreams_with_emotions.json", "r", encoding="utf-8") as f:
    dreams = json.load(f)

# 5. 프롬프트 템플릿 (논문 내용만 기반으로 답변하도록 강제)
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
다음은 사용자의 꿈 일기입니다:
"{question}"

다음은 Qdrant에서 검색된 관련 논문 내용입니다:
"{context}"

위 논문 내용을 반드시 기반으로 하여 사용자의 심리 상태를 해석해주세요.

📌 아래 규칙을 반드시 지켜야 합니다:
- 논문에 없는 내용은 절대 유추하지 마세요.
- 논문 출처를 바탕으로 분석이 어떻게 연결되는지 설명하세요.
- 허위 정보를 만들거나 추측하지 마세요.
- 응답은 따뜻하고 공감 가는 말투로, 심리학적 관점에서 해석해주세요.
"""
)

# 6. RAG 체인 구성 (Runnable 방식)
rag_chain = (
    RunnableMap({
        "context": lambda x: "\n\n".join([doc.page_content for doc in x["input_documents"]]),
        "question": lambda x: x["question"]
    })
    | prompt_template
    | llm
)

# 7. 꿈 해몽 실행
for i, dream in enumerate(dreams[:3]):
    query = dream["content"]
    print(f"\n🔍 [사용자 질문 {i+1}]: {dream['title']}")

    # 🔍 Qdrant 문서 검색
    docs = vectorstore.as_retriever().get_relevant_documents(query)
    print(f"📚 검색된 문서 수: {len(docs)}")

    # ✅ Qdrant 검색 결과 확인 (테스트용)
    print("\n📄 🔍 검색된 문서 미리보기:")
    for j, doc in enumerate(docs):
        print(f"📄 문서 {j+1}: {doc.metadata.get('title')}")
        print(doc.page_content[:300], "\n---")

    # 🧠 해몽 생성
    result = rag_chain.invoke({
        "input_documents": docs,
        "question": query
    })
    print("\n🧠 해몽 응답:")
    print(result.content if hasattr(result, 'content') else result)
