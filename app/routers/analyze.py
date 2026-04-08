import httpx
from fastapi import APIRouter, HTTPException
from app.models.request_models import (
    AnalyzeRequest,
    AnalyzeResponse,
    GitHubFetchRequest,
    GitHubFetchResponse,
    ReviewRequest,
    ReviewResponse,
)
from app.services.code_analysis_service import CodeAnalysisService
from app.services.ai_service import AIService
from app.services.github_fetch_service import GitHubFetchError, fetch_github_file
from app.providers.openai_provider import OpenAIProvider

router = APIRouter(prefix="/api")


def get_code_analysis_service(api_key: str) -> CodeAnalysisService:
    provider = OpenAIProvider(api_key=api_key)
    ai_service = AIService(provider=provider)
    return CodeAnalysisService(ai_service=ai_service)


@router.post("/analyze-code", response_model=AnalyzeResponse)
async def analyze_code(
    request: AnalyzeRequest
):
    service = get_code_analysis_service(request.api_key)
    return await service.analyze_code(request.code, request.analysis_standard)


@router.post("/review-user-fix", response_model=ReviewResponse)
async def review_user_fix(
    request: ReviewRequest
):
    service = get_code_analysis_service(request.api_key)
    return await service.review_user_fix(
        original_code=request.original_code,
        user_fix=request.user_fix
    )


@router.post("/fetch-github", response_model=GitHubFetchResponse)
async def fetch_github(request: GitHubFetchRequest):
    try:
        code, filename = await fetch_github_file(request.url)
    except GitHubFetchError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=502,
            detail="Nie udało się pobrać pliku z GitHub. Spróbuj ponownie.",
        ) from e
    return GitHubFetchResponse(code=code, filename=filename)


@router.get("/health")
async def health():
    return {"status": "ok"}