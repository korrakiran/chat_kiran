from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from ..services.ocr import OCRService
from typing import Dict

router = APIRouter()
ocr_service = OCRService()

@router.post("/")
async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    content = await file.read()
    filename = file.filename.lower()
    
    try:
        if filename.endswith(".pdf"):
            extracted_text = ocr_service.extract_text_from_pdf(content)
        elif filename.endswith((".png", ".jpg", ".jpeg")):
            extracted_text = ocr_service.extract_text_from_image(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
            
        return {"filename": file.filename, "extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
