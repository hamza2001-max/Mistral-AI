import express from 'express';
import dotenv from 'dotenv';
import cors from "cors";
import MistralClient from '@mistralai/mistralai';

dotenv.config();
const app = express();
const port = process.env.PORT || 5000;
const corsOptions = {
  origin: process.env.BASE_URL,
  credentials: true,
};
app.use(cors(corsOptions));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.post('/api/chat', async (req, res) => {
  const question = req.body.question;
  const apiKey = process.env.MISTRAL_API_KEY;
  const model = "mistral-large-latest";

  const client = new MistralClient(apiKey);
  try {
    const response = await client.chat({
      model,
      messages: [{ role: 'user', content: question}],
    }); 
    res.json({ success: true, answer: response.choices[0].message.content });
  } catch (error) {
    console.error(error);
    res.json({ success: false, error: 'An error occurred while processing your request.' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
