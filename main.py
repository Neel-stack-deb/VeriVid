import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import health, upload, videos
from app.core.config import settings
from app.schemas.api_errors import ErrorResponse

logging.basicConfig(level=logging.INFO)

app = FastAPI(
  title=settings.app_name,
  description="VeriVid multimodal video intelligence API",
  version="0.2.0",
)

if settings.cors_origins:
  app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )

app.include_router(router=health.router)
app.include_router(router=upload.router)
app.include_router(router=videos.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(
  request: Request,
  exc: Exception,
) -> JSONResponse:
  logging.getLogger(__name__).exception(
    "Unhandled error on %s %s",
    request.method,
    request.url.path,
  )
  body = ErrorResponse(detail="Internal server error", code="internal_error")
  return JSONResponse(status_code=500, content=body.model_dump())


def main():
  print(f"Hello from {settings.app_name}")


if __name__ == "__main__":
  main()