import json

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.vector_store import vector_store


class DocumentManager:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def load_pdf(self, pdf_path):
        """
        Load a single PDF from disk.
        """

        loader = PyPDFLoader(str(pdf_path))

        return loader.load()

    def split_documents(self, documents):
        """
        Split documents into chunks.
        """

        return self.splitter.split_documents(documents)

    def save_chunks(self, chunks):
        """
        Save chunks for debugging/inspection.
        """

        data = []

        for chunk in chunks:

            data.append(
                {
                    "page_content": chunk.page_content,
                    "metadata": chunk.metadata
                }
            )

        with open(
            "app/storage/chunks.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False
            )

    def ingest_pdf(self, pdf_path):
        """
        Complete ingestion pipeline.
        """

        # Load PDF
        documents = self.load_pdf(pdf_path)

        # Split into chunks
        chunks = self.split_documents(documents)

        # Save chunks (optional, useful for debugging)
        self.save_chunks(chunks)

        # Store embeddings in PGVector
        vector_store.add_documents(chunks)

        return {
            "documents": len(documents),
            "chunks": len(chunks)
        }


# Shared instance
document_manager = DocumentManager()