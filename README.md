# hydrapi
multiheaded hydrator in railway-fastapi

# Directory structure:
# hydrapi/
# ├── requirements.txt
# ├── main.py
# ├── Procfile
# ├── runtime.txt
# └── .gitignore

# requirements.txt
fastapi==0.103.1
uvicorn==0.23.2
python-multipart==0.0.6
pydantic==2.3.0

# main.py
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, List, Optional
import os

app = FastAPI(title="Architecture Pattern Detector")

# Basic API key auth - in production, use more secure methods
API_KEY = os.getenv("API_KEY", "your-default-api-key")

class ArchitectureRequest(BaseModel):
    files: List[str]
    directories: List[str]
    config_files: Optional[Dict[str, str]] = None

class ArchitectureResponse(BaseModel):
    detected_framework: str
    confidence: float
    markers: List[str]
    warnings: Optional[List[str]] = None

def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.get("/")
async def root():
    return {"message": "Architecture Pattern Detector API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/detect", response_model=ArchitectureResponse)
async def detect_architecture(request: ArchitectureRequest, api_key: str = Header(...)):
    verify_api_key(api_key)
    
    # Simple demo detection logic
    # In reality, you'd have more sophisticated pattern matching
    markers = []
    
    if "next.config.js" in request.files:
        return ArchitectureResponse(
            detected_framework="Next.js",
            confidence=0.9,
            markers=["next.config.js", "pages directory"],
            warnings=["Multiple routing systems detected"] if "react-router" in str(request.config_files) else None
        )
    
    if "angular.json" in request.files:
        return ArchitectureResponse(
            detected_framework="Angular",
            confidence=0.85,
            markers=["angular.json", "src/app directory"],
            warnings=None
        )
    
    return ArchitectureResponse(
        detected_framework="Unknown",
        confidence=0.1,
        markers=request.files[:5],  # First 5 files as example markers
        warnings=["Could not confidently detect framework"]
    )

# Procfile
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# runtime.txt
python-3.9.16

# .gitignore
__pycache__/
*.py[cod]
*$py.class
.env
.venv
env/
venv/
ENV/


# Init
git init
git add .
git commit -m "Initial commit"

# Deploy to Railway:

Create a new Railway project
Connect your GitHub repository
Railway will automatically detect the Python app and deploy it

Set your environment variables in Railway:

Add API_KEY with your chosen key

# Health check
curl https://your-app-url/health

# Detect architecture
curl -X POST https://your-app-url/detect \
  -H "Content-Type: application/json" \
  -H "api-key: your-api-key" \
  -d '{"files": ["next.config.js"], "directories": ["pages"], "config_files": {}}'
