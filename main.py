from app.core.config import settings 
from fastapi import FastAPI
from app.api import health
app = FastAPI(
    title=settings.app_name,
    description="VeriVid API",
    version="0.1.0",
)

app.include_router(
    router = health.router
)

def main():
    print(f"Hello from {settings.app_name}")


if __name__ == "__main__":
    main()
