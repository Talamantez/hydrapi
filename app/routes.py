# app/routes.py
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
from app.core.config import settings

router = APIRouter()

class ArchitectureRequest(BaseModel):
    files: List[str]
    directories: List[str]
    config_files: Optional[Dict[str, str]] = None

class ArchitectureResponse(BaseModel):
    detected_framework: str
    confidence: float
    markers: List[str]
    warnings: Optional[List[str]] = None

@router.get("/")
async def root():
    return {"message": "Architecture Pattern Detector API", "status": "running"}

@router.post("/detect", response_model=ArchitectureResponse)
async def detect_architecture(request: ArchitectureRequest, api_key: str = Header(...)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    if "next.config.js" in request.files:
        return ArchitectureResponse(
            detected_framework="Next.js",
            confidence=0.9,
            markers=["next.config.js", "pages directory"],
            warnings=["Multiple routing systems detected"] if "react-router" in str(request.config_files) else None
        )
    
    # Add other framework detection logic here
    
    return ArchitectureResponse(
        detected_framework="Unknown",
        confidence=0.1,
        markers=request.files[:5],
        warnings=["Could not confidently detect framework"]
    )