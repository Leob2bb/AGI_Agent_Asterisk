import os
import json
from dotenv import load_dotenv
from langchain_upstage import ChatUpstage
from langchain_upstage.embeddings import UpstageEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

# 1. 환경 변수 로드
load_dotenv()
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
assert UPSTAGE_API_KEY, "❌ .env에 UPSTAGE_API_KEY가 필요합니다."

# 2. Qdrant 벡터DB 연결
qdrant = QdrantVectorStore(
    client=QdrantClient(host="localhost", port=6333),
    collection_name="dream-papers",
    embedding=UpstageEmbeddings(api_key=UPSTAGE_API_KEY, model="embedding-passage")
)

# 3. Upstage LLM (GPT 대체)
llm = ChatUpstage(api_key=UPSTAGE_API_KEY, model="solar-1-mini-chat")

# 4. 사용자 질문 불러오기
with open("dreams_with_emotions.json", "r", encoding="utf-8") as f:
    dreams = json.load(f)

# 5. 프롬프트 템플릿 (질문과 문맥을 함께 전달)
prompt_template = PromptTemplate.from_template("""
다음은 사용자의 꿈 일기입니다:
"{context}"

이 사람의 심리 상태를 분석하고, 관련된 논문 지식을 활용해서 해석해 주세요. 분석 내용은 친절하고 구체적으로 작성해주세요.
""")

# 6. RAG 체인 구성
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=qdrant.as_retriever(search_kwargs={"k": 3}),
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt_template}
)

# 7. 사용자 꿈 데이터에 대해 응답 생성
for i, dream in enumerate(dreams[:3]):  # 테스트용으로 3개만 처리
    query = dream["content"]
    print(f"\n🔍 [사용자 질문 {i+1}]: {dream['title']}")
    print("🧠 RAG 응답:")
    result = rag_chain.run(query)
    print(result)
