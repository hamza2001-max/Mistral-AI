from dotenv import load_dotenv
import streamlit as st
from mistralai.models.chat_completion import ChatMessage
import os
# from audio_recorder_streamlit import audio_recorder
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

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        print("Sorry, could not recognize the audio")
        return None

def get_chat_response(question):
    messages = [
        ChatMessage(role="user", content=question)
    ]

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

st.title("Ask Mistral AI anything.");

for message in st.session_state.conversation:
	if isinstance(message, AIMessage):
		with st.chat_message('AI'):
			st.markdown(message.content)
	else:
		with st.chat_message('Human'):
			st.markdown(message)
                  

user_input = st.chat_input("You may ask....");

@st.experimental_fragment
def process():
    st.session_state.conversation.append(HumanMessage(content=user_input))
    with st.chat_message('Human'):
        st.markdown(user_input)
    
    with st.chat_message('AI'):
        response = get_chat_response(user_input);
        st.session_state.response = response;
        st.write(f"Answer: {response}");
        st.session_state.conversation.append(AIMessage(content=response));
        if st.button("🔊"):
            if st.session_state.response:
                text_to_speech(st.session_state.response)

# footer_container = st.container()
# with footer_container:
#     audio_bytes = audio_recorder()

# if audio_bytes:
#     with st.spinner("Transcribing..."):
#         webm_file_path = "temp_audio.mp3"
#         if webm_file_path:
#             with open(webm_file_path, "wb") as f:
#                 f.write(audio_bytes)
#         transcript = speech_to_text(webm_file_path)
#         if transcript:
#             with st.chat_message("user"):
#                 st.write(transcript)
#             with st.chat_message('AI'):
#                 response = get_chat_response(transcript);
#                 st.markdown(response);
#             os.remove(webm_file_path)

if user_input is not None and user_input.strip() != "":
    process()
