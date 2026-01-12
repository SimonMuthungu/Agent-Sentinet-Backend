# app/api/uploads.py
import logging
from fastapi import APIRouter, UploadFile
from app.services.vectorstore import embed_and_upsert
from app.services.documents import extract_text_from_pdf  # create this helper

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/vendors/{vendor_id}/upload")
async def upload_vendor_doc(vendor_id: str, file: UploadFile):
    print('Document uploaded for upserting')
    content = await file.read()
    text = extract_text_from_pdf(content)
    embed_and_upsert(vendor_id, [text])
    logger.info(f"Uploaded and indexed doc for vendor {vendor_id}")
    return {"ok": True}