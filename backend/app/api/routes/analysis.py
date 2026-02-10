from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from PIL import Image
import io
from app.services.gemini_service import check_relevance, analyze_oncology

router = APIRouter()

@router.post("/ai-analyze")
async def analyze_case(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    if not file and not text:
        raise HTTPException(status_code=400, detail="Please provide at least an image or text input.")

    content_parts = []
    
    # Process text
    if text:
        content_parts.append(text)
        
    # Process image
    if file:
        try:
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            content_parts.append(image)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

    # 1. Guardrail Check
    is_relevant, reason = await check_relevance(content_parts)
    
    if not is_relevant:
        return {
            "is_relevant": False,
            "reason": reason,
            "analysis": None,
            "chart_data": None
        }

    # 2. Oncology Analysis
    analysis_text, chart_data = await analyze_oncology(content_parts)

    return {
        "is_relevant": True,
        "reason": "Analysis successful",
        "analysis": analysis_text,
        "chart_data": chart_data
    }
