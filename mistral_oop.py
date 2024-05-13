import os
from dotenv import load_dotenv
import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import pyttsx3
from langchain_core.messages import AIMessage, HumanMessage

load_dotenv(".env")
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

class Chatbot:
    def __init__(self):
        self.client = MistralClient(api_key=api_key)
        self.conversation = [
            AIMessage(content="Ask me anything!")
        ]
        self.user_question = ""
        self.response = ""

    def text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def get_chat_response(self, question):
        messages = [
            ChatMessage(role="user", content=question)
        ]

        chat_response = self.client.chat(
            model=model,
            messages=messages,
        )

        return chat_response.choices[0].message.content

    def display_conversation(self):
        for message in self.conversation:
            if isinstance(message, AIMessage):
                with st.chat_message('AI'):
                    st.markdown(message.content)
            else:
                with st.chat_message('Human'):
                    st.markdown(message)
    @st.experimental_fragment
    def process(self, user_input):
        self.conversation.append(HumanMessage(content=user_input))
        with st.chat_message('Human'):
            st.markdown(user_input)

        with st.chat_message('AI'):
            response = self.get_chat_response(user_input)
            self.response = response
            st.write(f"Answer: {response}")
            self.conversation.append(AIMessage(content=response))
            if st.button("🔊"):
                if self.response:
                    self.text_to_speech(self.response)

if __name__ == '__main__':
    chatbot = Chatbot()
    st.title("Ask Mistral AI anything.")
    chatbot.display_conversation()

    user_input = st.chat_input("You may ask....")

    if user_input is not None and user_input.strip() != "":
        chatbot.process(user_input)
