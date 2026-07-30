from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from app.auth.security import get_current_user
from app.services.storage_service import storage_service
from app.rag.document_manager import document_manager

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    # Only allow PDF files
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    try:
        # Step 1: Upload to Supabase Storage
        storage_info = await storage_service.upload_pdf(file)

        # Step 2: Download temporarily for processing
        temp_path = storage_service.download_pdf(
            storage_info["stored_name"]
        )

        # Step 3: Chunk + Embed + Store in PGVector
        stats = document_manager.ingest_pdf(temp_path)

        # Step 4: Delete temporary file
        if temp_path.exists():
            temp_path.unlink()

        return {
            "message": "Document uploaded and indexed successfully.",
            "document": storage_info,
            "ingestion": stats
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("")
async def get_documents(
    current_user=Depends(get_current_user)
):
    try:
        documents = storage_service.list_documents()
        return documents

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )