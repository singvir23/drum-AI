const express = require("express");
const cors = require("cors");
const OpenAI = require("openai");

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY // Ensure the API key is either passed via environment variables
});

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

app.post("/generate-xml", async (req, res) => {
  const { prompt } = req.body;

  try {
    const completion = await openai.chat.completions.create({
      model: "ft:gpt-4o-2024-08-06:personal::A8KaeVnK", 
      messages: [
        { role: "system", content: "You are a helpful assistant who generates MusicXML code. Only return valid MusicXML." },
        { role: "user", content: prompt + ". Provide this prompt in musicxml code for the snare drum" },
      ],
    });

    const xmlOutput = completion.choices[0].message.content;

    res.json({ xml: xmlOutput });
  } catch (error) {
    console.error("Error generating MusicXML: ", error);
    res.status(500).json({ error: "Error generating MusicXML" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
