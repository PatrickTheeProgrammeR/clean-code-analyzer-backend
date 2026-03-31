from fastapi import APIRouter, Depends
from app.models.request_models import (
    AnalyzeRequest,
    AnalyzeResponse,
    ReviewRequest,
    ReviewResponse
)
from app.services.code_analysis_service import CodeAnalysisService
from app.services.ai_service import AIService
from app.providers.openai_provider import OpenAIProvider

router = APIRouter(prefix="/api")


def get_code_analysis_service() -> CodeAnalysisService:
    provider = OpenAIProvider()
    ai_service = AIService(provider=provider)
    return CodeAnalysisService(ai_service=ai_service)


@router.post("/analyze-code", response_model=AnalyzeResponse)
async def analyze_code(
    request: AnalyzeRequest,
    service: CodeAnalysisService = Depends(get_code_analysis_service)
):
    return await service.analyze_code(request.code)


@router.post("/review-user-fix", response_model=ReviewResponse)
async def review_user_fix(
    request: ReviewRequest,
    service: CodeAnalysisService = Depends(get_code_analysis_service)
):
    return await service.review_user_fix(
        original_code=request.original_code,
        user_fix=request.user_fix
    )


@router.get("/health")
async def health():
    return {"status": "ok"}