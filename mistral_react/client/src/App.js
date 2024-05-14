import React, { useEffect, useState } from "react";
import axios from "axios";
import { HiMiniSpeakerWave } from "react-icons/hi2";
import { IoStop, IoSend } from "react-icons/io5";
import { AiFillAudio, AiOutlineAudioMuted } from "react-icons/ai";
import { GrPowerReset } from "react-icons/gr";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import toast, { Toaster } from 'react-hot-toast';




function App() {
  const [conversation, setConversation] = useState([
    { role: "AI", content: "Ask me anything!" },
  ]);
  const [userQuestion, setUserQuestion] = useState("");
  const { transcript, resetTranscript } = useSpeechRecognition();
  const [speechSupportMessage, setSpeechSupportMessage] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);

  const inputError = () => toast('Input cannot be empty.')
  const handleUserQuestionChange = (event) => {
    setUserQuestion(event.target.value);
  };

  useEffect(() => {
    if (!SpeechRecognition.browserSupportsSpeechRecognition()) {
      setSpeechSupportMessage(
        "Sorry, speech recognition is not supported in your browser. You can use chrome."
      );
    }
  }, []);

  const handleSubmit = async (question) => {
    // console.log(value);
    try {
      if(question.length === 0){
        throw new Error("Question cannot be empty");
      }
      const response = await axios.post(
        "http://localhost:5000/api/chat",
        { question },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (response.data.success) {
        setConversation((prev) => [
          ...prev,
          { role: "AI", content: response.data.answer },
        ]);
        setUserQuestion("");
      }
    } catch (error) {
      inputError();
    }
  };

  const submitText = (event) => {
    event.preventDefault();
    setConversation((prev) => [
      ...prev,
      { role: "Human", content: userQuestion },
    ]);
    handleSubmit(userQuestion);
  };

  const submitAudio = (event) => {
    event.preventDefault();
    setIsListening(false);
    SpeechRecognition.stopListening();
    console.log(transcript);
    setConversation((prev) => [
      ...prev,
      { role: "Human", content: transcript },
    ]);
    handleSubmit(transcript);
  };

  const textToSpeech = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
    setIsSpeaking(true);
    utterance.onend = () => {
      setIsSpeaking(false);
    };
  };

  const stopSpeaking = () => {
    speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  return (
    <div className="container relative">
      <Toaster/>
      <div className="mt-8">
        <h3 className="text-3xl font-bold mb-3">Ask Mistral AI anything.</h3>
        {conversation.map((message, index) => (
          <div key={index} className="mb-2">
            <p className={message.role === "AI" ? "font-normal" : "font-bold"}>
              {message.content}
            </p>
            {message.role === "AI" && index !== 0 && (
              <>
                {!isSpeaking ? (
                  <button onClick={() => textToSpeech(message.content)}>
                    <HiMiniSpeakerWave className="text-xl" />
                  </button>
                ) : (
                  <button onClick={stopSpeaking}>
                    <IoStop />
                  </button>
                )}
              </>
            )}
          </div>
        ))}
      </div>
      <form onSubmit={submitText} className="fixed bottom-8 ">
        <div className="container flex items-center space-x-3">
          <input
            onChange={handleUserQuestionChange}
            placeholder="Ask a question..."
            className="w-[50rem] p-3 border border-gray-300 rounded bg-white "
          />
          <button
            type="submit"
            className="bg-blue-500 hover:bg-blue-600 text-white p-3 rounded"
          >
            <IoSend className="text-xl" />
          </button>
          <div>
            {speechSupportMessage ? (
              speechSupportMessage
            ) : (
              <>
                {isListening ? (
                  <div className="flex space-x-3">
                    <button
                    className="bg-blue-500 hover:bg-blue-600 text-white p-3 rounded"
                    onClick={submitAudio}><AiOutlineAudioMuted className="text-xl" /></button>
                    <button
                    className="bg-blue-500 hover:bg-blue-600 text-white p-3 rounded"
                      onClick={() => {
                        setIsListening(false);
                        resetTranscript();
                      }}
                    >
                      <GrPowerReset className="text-xl" />
                    </button>
                  </div>
                ) : (
                  <button
                    className="bg-blue-500 hover:bg-blue-600 text-white p-3 rounded"
                    onClick={() => {
                      SpeechRecognition.startListening();
                      setIsListening(true);
                    }}
                  >
                    <AiFillAudio className="text-xl" />
                  </button>
                )}
              </>
            )}
          </div>
        </div>
      </form>
    </div>
  );
}

export default App;
