from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers.analyze import router
from app.exceptions import AIProviderError, InvalidAIResponseError

app = FastAPI(title="Clean Code Analyzer")

raw_allowed_origins = os.getenv("CORS_ALLOW_ORIGINS", "")
allow_origins = [origin.strip() for origin in raw_allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


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