import { useEffect, useState } from "react";

import api from "../api/axios";

import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

export default function Chat() {

    const [messages, setMessages] = useState([
        {
            role: "assistant",
            content: "Hello! Ask me anything about your uploaded documents.",
            sources: []
        }
    ]);

    const [documents, setDocuments] = useState([]);

    useEffect(() => {
        loadDocuments();
    }, []);

    async function loadDocuments() {

        try {

            const response = await api.get("/documents");

            setDocuments(response.data);

        } catch (err) {

            console.error(err);

        }

    }

    return (

        <div className="flex h-screen bg-slate-950">

            <Sidebar
                documents={documents}
                refreshDocuments={loadDocuments}
            />

            <div className="flex flex-col flex-1">

                <Navbar />

                <ChatWindow
                    messages={messages}
                />

                <ChatInput
                    setMessages={setMessages}
                />

            </div>

        </div>

    );

}