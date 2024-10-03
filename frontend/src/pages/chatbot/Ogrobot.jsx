import React, { useState } from "react";
import { GoogleGenerativeAI } from "@google/generative-ai";

// Style components using Tailwind CSS
import "../../style/ogrobot.css";
import ChatHistory from "./ChatHistory";
import Loading from "./Loading";

const Ogrobot = () => {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // Initialize your Gemini API
  const genAI = new GoogleGenerativeAI(import.meta.env.VITE_GOOGLE_GEN_AI_KEY);
  const model = genAI.getGenerativeModel({
    model: import.meta.env.VITE_GOOGLE_GEN_AI_MODEL,
    systemInstruction: import.meta.env.VITE_GOOGLE_GEN_AI_INSTRUCTION,
  });

  // Function to handle user input
  const handleUserInput = (e) => {
    setUserInput(e.target.value);
  };

  // Function to send user message to Gemini
  const sendMessage = async () => {
    if (userInput.trim() === "") return;

    setIsLoading(true);
    try {
      // Call Gemini API to get a response
      const result = await model.generateContent(userInput);
      const response = await result.response;
      console.log(response);
      // Add Gemini's response to the chat history
      setChatHistory([
        ...chatHistory,
        { type: "user", message: userInput },
        { type: "bot", message: response.text() },
      ]);
    } catch {
      console.error("Error sending message");
    } finally {
      setUserInput("");
      setIsLoading(false);
    }
  };

  // Function to clear the chat history
  const clearChat = () => {
    setChatHistory([]);
  };

  return (
    <div className="container">
      <h1 className="text-3xl font-bold text-green-800 text-center mb-4">
        OgrodutBot
      </h1>

      <div className="chat-container rounded-lg shadow-lg p-4">
        <ChatHistory chatHistory={chatHistory} />
        <Loading isLoading={isLoading} />
      </div>

      <div className="flex mt-4">
        <input
          type="text"
          className="flex-grow px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500"
          placeholder="Type your message..."
          value={userInput}
          onChange={handleUserInput}
        />
        <button
          className="px-4 py-2 ml-2 rounded-lg bg-green-800 text-white hover:bg-[#79806c] focus:outline-none"
          onClick={sendMessage}
          disabled={isLoading}
        >
          Send
        </button>
      </div>

      {/* Centered Clear Chat Button */}
      <div className="flex justify-center mt-4">
        <button
          className="px-4 py-2 rounded-lg bg-green-800 text-white hover:bg-[#79806c] focus:outline-none"
          onClick={clearChat}
        >
          Clear Chat
        </button>
      </div>
    </div>
  );
};

export default Ogrobot;
