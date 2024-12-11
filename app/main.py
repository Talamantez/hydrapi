from fastapi import FastAPI
from app.core.config import settings
from app.routes import router

app = FastAPI(
    title="Architecture Pattern Detector",
    docs_url="/docs" if settings.ENV != "production" else None
)

app.include_router(router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}