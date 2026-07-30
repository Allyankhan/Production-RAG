from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from supabase import create_client, Client

from app.config import settings

# ---------------------------------
# Initialize Supabase Client
# ---------------------------------
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY
)


class StorageService:

    def __init__(self):
        self.bucket = settings.SUPABASE_BUCKET

    async def upload_pdf(self, file: UploadFile):
        """
        Upload a PDF to Supabase Storage.
        """

        extension = Path(file.filename).suffix if file.filename else ".pdf"

        filename = f"{uuid4()}{extension}"

        contents = await file.read()

        supabase.storage.from_(self.bucket).upload(
            path=filename,
            file=contents,
            file_options={
                "content-type": file.content_type or "application/pdf"
            }
        )

        return {
            "stored_name": filename,
            "original_name": file.filename,
            "bucket": self.bucket,
            "content_type": file.content_type
        }

    def download_pdf(self, filename: str) -> Path:
        """
        Download a PDF from Supabase Storage
        into a temporary local folder.
        """

        data = supabase.storage.from_(self.bucket).download(filename)

        temp_dir = Path("storage/temp")
        temp_dir.mkdir(parents=True, exist_ok=True)

        file_path = temp_dir / filename

        with open(file_path, "wb") as f:
            f.write(data)

        return file_path

    def list_documents(self):
        """
        Return all uploaded documents from the Supabase bucket.
        """

        files = supabase.storage.from_(self.bucket).list()

        documents = []

        for file in files:

            documents.append(
                {
                    "id": file.get("id"),
                    "name": file.get("name"),
                    "updated_at": file.get("updated_at"),
                    "created_at": file.get("created_at"),
                    "last_accessed_at": file.get("last_accessed_at"),
                    "metadata": file.get("metadata", {})
                }
            )

        return documents


storage_service = StorageService()