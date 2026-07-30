import api from "../api/axios";

export default function Sidebar({

    documents,

    refreshDocuments

}) {

    async function uploadFile(e) {

        const file = e.target.files[0];

        if (!file) return;

        const formData = new FormData();

        formData.append("file", file);

        try {

            await api.post(
                "/documents/upload",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            // Reload document list
            await refreshDocuments();

        } catch (err) {

            console.error(err);

            alert("Upload failed.");

        }
    }

    return (

        <div className="w-72 bg-slate-900 border-r border-slate-700 text-white flex flex-col">

            {/* Header */}

            <div className="p-6 border-b border-slate-700">

                <h1 className="text-2xl font-bold">

                    Production RAG

                </h1>

                <p className="text-sm text-slate-400 mt-2">

                    AI Document Assistant

                </p>

            </div>

            {/* Documents */}

            <div className="flex-1 overflow-y-auto p-5">

                <h2 className="font-semibold mb-4">

                    Documents

                </h2>

                {
                    documents.length === 0 ? (

                        <p className="text-slate-400 text-sm">

                            No documents uploaded.

                        </p>

                    ) : (

                        <div className="space-y-2">

                            {

                                documents.map((doc) => (

                                    <div
                                        key={doc.name}
                                        className="bg-slate-800 rounded-lg p-3 hover:bg-slate-700 transition"
                                    >

                                        📄 {doc.name}

                                    </div>

                                ))

                            }

                        </div>

                    )
                }

            </div>

            {/* Upload */}

            <div className="p-5 border-t border-slate-700">

                <label
                    className="block text-center bg-cyan-600 hover:bg-cyan-700 cursor-pointer rounded-lg py-3 font-medium transition"
                >

                    Upload PDF

                    <input
                        type="file"
                        accept=".pdf"
                        className="hidden"
                        onChange={uploadFile}
                    />

                </label>

            </div>

        </div>

    );

}