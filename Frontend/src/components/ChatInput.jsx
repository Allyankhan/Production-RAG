import { useState } from "react";
import api from "../api/axios";

export default function ChatInput({ setMessages }) {

    const [question, setQuestion] = useState("");

    const [loading, setLoading] = useState(false);

    async function sendMessage() {

        if (!question.trim()) return;

        const currentQuestion = question;

        // Add user message immediately
        setMessages(prev => [
            ...prev,
            {
                role: "user",
                content: currentQuestion
            }
        ]);

        setQuestion("");

        setLoading(true);

        try {

            const response = await api.post(
                "/chat",
                {
                    question: currentQuestion
                }
            );

            setMessages(prev => [
                ...prev,
                {
                    role: "assistant",
                    content: response.data.answer,
                    sources: response.data.sources || []
                }
            ]);

        } catch (err) {

            console.error(err);

            const errorMessage =
                err.response?.data?.detail ||
                "Something went wrong.";

            setMessages(prev => [
                ...prev,
                {
                    role: "assistant",
                    content: errorMessage,
                    sources: []
                }
            ]);

        } finally {

            setLoading(false);

        }

    }

    function handleKeyDown(e) {

        if (e.key === "Enter" && !loading) {

            sendMessage();

        }

    }

    return (

        <div className="border-t border-slate-700 bg-slate-900 p-5 flex gap-3">

            <input
                className="flex-1 bg-slate-800 rounded-lg px-5 py-3 text-white outline-none"
                placeholder="Ask anything about your documents..."
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
            />

            <button
                onClick={sendMessage}
                disabled={loading}
                className="bg-cyan-600 hover:bg-cyan-700 disabled:bg-slate-700 text-white px-6 rounded-lg font-semibold transition"
            >

                {loading ? "Thinking..." : "Send"}

            </button>

        </div>

    );

}