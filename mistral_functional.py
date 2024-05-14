from dotenv import load_dotenv
import streamlit as st
from mistralai.models.chat_completion import ChatMessage
import os

import pyttsx3
from mistralai.client import MistralClient
from langchain_core.messages import AIMessage, HumanMessage
import speech_recognition as sr

load_dotenv(".env")
api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key);

def text_to_speech(text):
    engine = pyttsx3.init();
    engine.say(text);
    engine.runAndWait();


def transcribe_audio(audio_data):
    recognizer = sr.Recognizer()
    audio = sr.AudioData(audio_data, sample_rate=44100, sample_width=2)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Unable to recognize speech"
    except sr.RequestError as e:
        return "Error with the transcription service: {0}".format(e)


def get_chat_response(question):
    messages = [ChatMessage(role="user", content=question)]
    chat_response = client.chat(
        model=model,
        messages=messages,
    )
    return chat_response.choices[0].message.content



if 'conversation' not in st.session_state:
	st.session_state.conversation = [
		AIMessage(content="Ask me anything!")
	]
if 'user_question' not in st.session_state:
    st.session_state.user_question = ""
if 'response' not in st.session_state:
    st.session_state.response = ""

user_input = st.chat_input("You may ask....");

@st.experimental_fragment
def process(text):
    st.session_state.conversation.append(HumanMessage(content=text))
    with st.chat_message('Human'):
        st.markdown(text)
    with st.chat_message('AI'):
        response = get_chat_response(text);
        st.session_state.response = response;
        st.write(f"Answer: {response}");
        st.session_state.conversation.append(AIMessage(content=response));
        
audioText = "";

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        st.write("Listening....")
        audio = r.listen(source)
    try:
        audioText = r.recognize_google(audio)
        if audioText is not None and audioText.strip() != "":
            process(audioText)
    except sr.UnknownValueError:
        st.write("Sorry, could not understand audio.")
    except sr.RequestError as e:
        st.write(f"Error: {e}")


recording = False

col1, col2, col3 = st.columns([9, 1, 1])
with col1:
    st.title("Ask Mistral AI anything.");
with col2:
    if st.button("🎙️"):
        recording = True;
with col3:
    if st.button("🛑"):
        recording = False;
if recording:
    recognize_speech()


for message in st.session_state.conversation:
    if isinstance(message, AIMessage):
        with st.chat_message('AI'):
            st.markdown(message.content)
            if st.button("🔊", key=message):
                text_to_speech(message.content)
    else:
        with st.chat_message('Human'):
            st.markdown(message.content)


if user_input is not None and user_input.strip() != "":
    process(user_input);


