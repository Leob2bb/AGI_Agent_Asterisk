from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence


class Chatbot:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="solar-pro",  # solar-pro 모델 사용
            openai_api_key="up_iIFJ3o3pGBZt5KOdlSj2SCDnGizup",
            base_url="https://api.upstage.ai/v1"
        )

        # 자동 대화 기록 관리
        self.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )

        # 최신 ChatPromptTemplate 사용
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "너는 친절한 상담사야."),
            ("human", "{input}")
        ])

        # RunnableSequence로 프롬프트 → LLM 연결
        # self.chain = RunnableSequence(
        #     steps=[self.prompt, self.llm],
        #     input_schema={"input": str, "history": list},
        # )

    def get_chat_response(self, user_message):
        # memory.load_memory_variables는 dict로 {"history": [...]}
        memory_variables = self.memory.load_memory_variables({})
        inputs = {
            "input": user_message,
            "history": memory_variables["history"]
        }

        # invoke 실행
        response = self.chain.invoke(inputs)

        # 대화 내용 메모리에 기록
        self.memory.save_context({"input": user_message}, {"output": response.content})

        print(response.content)
        return response.content


# Example Usage
if __name__ == "__main__":
    chatbot = Chatbot()
    while True:
        user_input = input("User: ")
        if user_input.lower() in ("exit", "quit"):
            break
        chat_response = chatbot.get_chat_response(user_input)
        print("\nAI Response:", chat_response)
