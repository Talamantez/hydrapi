from fastapi import FastAPI, APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.core.config import settings

router = APIRouter()

# Data models
class ArchitectureRequest(BaseModel):
    files: List[str]
    directories: List[str]
    config_files: Optional[Dict[str, str]] = None

class ArchitectureResponse(BaseModel):
    detected_framework: str
    confidence: float
    markers: List[str]
    warnings: Optional[List[str]] = None
    tier: Optional[str] = "free"
    remaining_quota: Optional[int] = None

class UsageMetrics(BaseModel):
    timestamp: datetime
    user_id: str
    operation: str
    model: str
    tokens_used: int
    latency_ms: int
    status: str
    metadata: Optional[Dict[str, Any]] = None

class UsageSummary(BaseModel):
    daily_tokens: int
    monthly_tokens: int
    remaining_quota: int
    tier: str

class QuotaInfo(BaseModel):
    tier: str
    daily_limit: int
    monthly_limit: int
    features: List[str]

# Pricing tiers configuration
PRICING_TIERS = {
    "free": QuotaInfo(
        tier="free",
        daily_limit=1000,
        monthly_limit=10000,
        features=["basic_detection"]
    ),
    "pro": QuotaInfo(
        tier="pro",
        daily_limit=10000,
        monthly_limit=100000,
        features=["advanced_detection", "confidence_scoring", "detailed_analysis"]
    ),
    "enterprise": QuotaInfo(
        tier="enterprise",
        daily_limit=100000,
        monthly_limit=1000000,
        features=["custom_patterns", "team_management", "priority_support"]
    )
}

def verify_api_key(api_key: str = Header(...)) -> str:
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

def get_user_tier(api_key: str) -> str:
    # TODO: Implement actual tier lookup based on API key
    # For now, return "free" tier
    return "free"

def check_quota(api_key: str) -> bool:
    # TODO: Implement actual quota checking
    # For now, always return True
    return True

@router.get("/")
async def root():
    return {"message": "Architecture Pattern Detector API", "status": "running"}

@router.post("/detect", response_model=ArchitectureResponse)
async def detect_architecture(request: ArchitectureRequest, api_key: str = Header(...)):
    verify_api_key(api_key)
    
    # Get user's tier and check quota
    user_tier = get_user_tier(api_key)
    if not check_quota(api_key):
        raise HTTPException(
            status_code=429,
            detail="Quota exceeded. Please upgrade your plan."
        )
    
    # Get tier features
    tier_info = PRICING_TIERS[user_tier]
    
    if "next.config.js" in request.files:
        return ArchitectureResponse(
            detected_framework="Next.js",
            confidence=0.9,
            markers=["next.config.js", "pages directory"],
            warnings=["Multiple routing systems detected"] if "react-router" in str(request.config_files) else None,
            tier=user_tier,
            remaining_quota=tier_info.daily_limit
        )
    
    if "angular.json" in request.files:
        return ArchitectureResponse(
            detected_framework="Angular",
            confidence=0.85,
            markers=["angular.json", "src/app directory"],
            warnings=None,
            tier=user_tier,
            remaining_quota=tier_info.daily_limit
        )
    
    return ArchitectureResponse(
        detected_framework="Unknown",
        confidence=0.1,
        markers=request.files[:5],
        warnings=["Could not confidently detect framework"],
        tier=user_tier,
        remaining_quota=tier_info.daily_limit
    )

@router.post("/metrics", response_model=None)
async def log_usage(metrics: UsageMetrics, api_key: str = Header(...)):
    verify_api_key(api_key)
    
    # TODO: Implement metrics storage in your database
    print(f"Usage logged: {metrics.dict()}")
    return {"status": "recorded"}

@router.get("/usage/summary", response_model=UsageSummary)
async def get_usage_summary(api_key: str = Header(...)):
    verify_api_key(api_key)
    user_tier = get_user_tier(api_key)
    tier_info = PRICING_TIERS[user_tier]
    
    # TODO: Implement actual usage tracking
    # For now, return dummy data based on tier
    return UsageSummary(
        daily_tokens=1000,
        monthly_tokens=25000,
        remaining_quota=tier_info.daily_limit,
        tier=user_tier
    )

@router.get("/pricing/tiers", response_model=Dict[str, QuotaInfo])
async def get_pricing_tiers():
    return PRICING_TIERS

@router.get("/quota", response_model=QuotaInfo)
async def get_quota_info(api_key: str = Header(...)):
    verify_api_key(api_key)
    user_tier = get_user_tier(api_key)
    return PRICING_TIERS[user_tier]