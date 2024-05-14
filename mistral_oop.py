from dotenv import load_dotenv
import streamlit as st
import os
from mistralai.models.chat_completion import ChatMessage
import pyttsx3
from mistralai.client import MistralClient
from langchain_core.messages import AIMessage, HumanMessage
import speech_recognition as sr

load_dotenv(".env")

class MistralAssistant:
    def __init__(self):
        self.api_key = os.environ["MISTRAL_API_KEY"]
        self.model = "mistral-large-latest"
        self.client = MistralClient(api_key=self.api_key)
        self.recognizer = sr.Recognizer()

    def text_to_speech(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def transcribe_audio(self, audio_data):
        recognizer = sr.Recognizer()
        audio = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Unable to recognize speech"
        except sr.RequestError as e:
            return f"Error with the transcription service: {e}"

    def get_chat_response(self, question):
        messages = [ChatMessage(role="user", content=question)]
        chat_response = self.client.chat(model=self.model, messages=messages)
        return chat_response.choices[0].message.content

    @st.experimental_fragment
    def process_text_input(self, text):
        st.session_state.conversation.append(HumanMessage(content=text))
        with st.chat_message('Human'):
            st.markdown(text)
        with st.chat_message('AI'):
            response = self.get_chat_response(text)
            st.session_state.response = response
            st.write(f"Answer: {response}")
            st.session_state.conversation.append(AIMessage(content=response))


    def process_audio_input(self, audio_data):
        try:
            audioText = self.recognizer.recognize_google(audio_data)
            if audioText and audioText.strip():
                st.session_state.conversation.append(HumanMessage(content=audioText))
                response = self.get_chat_response(audioText)
                st.session_state.response = response
                st.session_state.conversation.append(AIMessage(content=response))
        except sr.UnknownValueError:
            st.write("Sorry, could not understand audio.")
        except sr.RequestError as e:
            st.write(f"Error: {e}")

mistral_assistant = MistralAssistant()

if 'conversation' not in st.session_state:
    st.session_state.conversation = [AIMessage(content="Ask me anything!")]
if 'response' not in st.session_state:
    st.session_state.response = ""

user_input = st.chat_input("You may ask....")

recording = False
col1, col2, col3 = st.columns([9, 1, 1])
with col1:
    st.title("Ask Mistral AI anything.")
with col2:
    if st.button("🎙️"):
        recording = True
with col3:
    if st.button("🛑"):
        recording = False

if recording:
    with st.spinner("Listening...."):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio_data = r.listen(source)
        mistral_assistant.process_audio_input(audio_data)

for message in st.session_state.conversation:
    if isinstance(message, AIMessage):
        with st.chat_message('AI'):
            st.markdown(message.content)
            if st.button("🔊", key=message):
                mistral_assistant.text_to_speech(message)
    else:
        with st.chat_message('Human'):
            st.markdown(message)


if user_input and user_input.strip():
    mistral_assistant.process_text_input(user_input)
