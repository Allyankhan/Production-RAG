import { useEffect, useRef } from "react";

export default function ChatWindow({ messages }) {

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "smooth"
        });

    }, [messages]);

    return (

        <div className="flex-1 overflow-y-auto bg-slate-950 p-8">

            <div className="max-w-4xl mx-auto space-y-6">

                {

                    messages.map((message, index) => (

                        <div
                            key={index}
                            className={`flex ${
                                message.role === "user"
                                    ? "justify-end"
                                    : "justify-start"
                            }`}
                        >

                            <div
                                className={`max-w-2xl rounded-2xl px-5 py-4 shadow-lg ${
                                    message.role === "user"
                                        ? "bg-cyan-600 text-white"
                                        : "bg-slate-800 text-white"
                                }`}
                            >

                                <p className="whitespace-pre-wrap leading-7">

                                    {message.content}

                                </p>

                                {
                                    message.role === "assistant" &&
                                    message.sources &&
                                    message.sources.length > 0 && (

                                        <div className="mt-4 border-t border-slate-600 pt-3">

                                            <p className="text-xs text-slate-400 mb-2">

                                                Sources

                                            </p>

                                            {

                                                message.sources.map((source, i) => (

                                                    <div
                                                        key={i}
                                                        className="bg-slate-700 rounded-md px-3 py-2 mb-2 text-sm"
                                                    >

                                                        📄 <span className="font-semibold">

                                                            {source.file}

                                                        </span>

                                                        {

                                                            source.page && (

                                                                <span className="text-slate-300">

                                                                    {" "}— Page {source.page}

                                                                </span>

                                                            )

                                                        }

                                                    </div>

                                                ))

                                            }

                                        </div>

                                    )

                                }

                            </div>

                        </div>

                    ))

                }

                <div ref={bottomRef}></div>

            </div>

        </div>

    );

}