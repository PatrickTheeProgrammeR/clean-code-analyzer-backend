from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers.analyze import router
from app.exceptions import AIProviderError, InvalidAIResponseError

app = FastAPI(title="Clean Code Analyzer")

# Dev: Vite bywa na localhost lub 127.0.0.1 i na różnych portach (5173, 5174, …).
app.add_middleware(
    CORSMiddleware,
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