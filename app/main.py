from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers.analyze import router
from app.exceptions import AIProviderError, InvalidAIResponseError, InvalidCodeInputError

app = FastAPI(title="Clean Code Analyzer")


def _parse_origins(raw: str) -> list[str]:
    out: list[str] = []
    for part in raw.split(","):
        o = part.strip().strip('"').strip("'")
        if o:
            out.append(o)
    return out


_restrict = os.getenv("CORS_RESTRICT", "").strip().lower() in ("1", "true", "yes")
if _restrict:
    allow_origins = _parse_origins(os.getenv("CORS_ALLOW_ORIGINS", ""))
else:
    allow_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {"service": "clean-code-analyzer", "docs": "/docs", "health": "/api/health"}


@app.get("/health")
async def health_alias():
    return {"status": "ok"}


@app.exception_handler(AIProviderError)
async def ai_provider_error_handler(request, exc):
    return JSONResponse(
        status_code=502,
        content={"error": str(exc)}
    )


@app.exception_handler(InvalidAIResponseError)
async def invalid_response_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )


@app.exception_handler(InvalidCodeInputError)
async def invalid_code_input_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )
