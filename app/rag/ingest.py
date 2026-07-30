from app.rag.document_manager import DocumentManager

manager = DocumentManager()

documents = manager.load_documents()

chunks = manager.split_documents(documents)

manager.save_chunks(chunks)
vector_store.add_documents(chunks)