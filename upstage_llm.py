from openai import OpenAI  # openai==1.52.2


class Chatbot:

    def __init__(self):
        self.client = OpenAI(api_key="up_iIFJ3o3pGBZt5KOdlSj2SCDnGizup",
                             base_url="https://api.upstage.ai/v1")
        self.chat_history = [{
            "role":
            "system",
            "content":
            "You are a compassionate and professional psychological counselor. You provide empathetic, thoughtful, and non-judgmental responses to users who seek mental health support. Always encourage self-reflection and positive thinking, and offer practical coping strategies. If I ask a question in Korean, you must answer in Korean."
        }]

    def get_chat_response(self, user_message, stream=True):
        self.chat_history.append({"role": "user", "content": user_message})

        response = self.client.ChatCompletion.create(
            api_key=self.api_key,  # ✅ API 키 직접 전달
            base_url=self.base_url,  # ✅ base_url 직접 전달
            model="solar-pro",
            messages=self.chat_history,
            stream=stream)

        response_text = ""
        if stream:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    print(chunk.choices[0].delta.content, end="")
                    response_text += chunk.choices[0].delta.content
        else:
            response_text = response.choices[0].message.content

        self.chat_history.append({
            "role": "assistant",
            "content": response_text
        })
        return response_text


# Example Usage
if __name__ == "__main__":
    chatbot = Chatbot()
    user_input = input("User: ")
    chat_response = chatbot.get_chat_response(user_input, stream=False)
    print("\nAI Response:", chat_response)
