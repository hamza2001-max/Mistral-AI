import React, { useState } from "react";
import axios from "axios";
import { Container, TextField, Button, Typography, Box } from "@mui/material";
import { IoSend } from "react-icons/io5";
function App() {
  const [conversation, setConversation] = useState([
    { role: "AI", content: "Ask me anything!" },
  ]);
  const [userQuestion, setUserQuestion] = useState("");

  const handleUserQuestionChange = (event) => {
    setUserQuestion(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setConversation((prev) => [
      ...prev,
      { role: "Human", content: userQuestion },
    ]);

    try {
      console.log(userQuestion);
      const response = await axios.post(
        "http://localhost:5000/api/chat",
        { question: userQuestion },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      // log
      if (response.data.success) {
        setConversation((prev) => [
          ...prev,
          { role: "AI", content: response.data.answer },
        ]);
        setUserQuestion("");
      }
    } catch (error) {
      console.error(error);
    }
  };

  const textToSpeech = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(utterance);
  };

  return (
    <Container>
      <Box marginTop={"2rem"}>
        <Typography variant="h3" style={{ fontWeight: "bold" }} mb={3}>
          Ask Mistral AI anything.
        </Typography>
        {conversation.map((message, index) => (
          <Box key={index} mb={2}>
            <Typography
              variant="body1"
              style={{ fontWeight: message.role === "AI" ? "bold" : "normal" }}
            >
              {message.content}
            </Typography>
            {message.role === "AI" && (
              <Button onClick={() => textToSpeech(message.content)}>
                Audio
              </Button>
            )}
          </Box>
        ))}
      </Box>
      <form onSubmit={handleSubmit}>
        <Box
          position={"fixed"}
          zIndex={20}
          width={"50rem"}
          bottom={25}
          display={"flex"}
          alignItems={"center"}
        >
          <TextField
            value={userQuestion}
            onChange={handleUserQuestionChange}
            placeholder="Ask a question..."
            fullWidth
            margin="normal"
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            style={{
              marginTop: "0.5rem",
              marginLeft: "1rem",
              height: "3.4rem",
            }}
          >
            <IoSend fontSize={"1.4rem"} />
          </Button>
        </Box>
      </form>
    </Container>
  );
}

export default App;
