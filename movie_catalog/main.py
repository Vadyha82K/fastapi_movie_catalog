import logging

from fastapi import (
    FastAPI,
    Request,
)

from api import router as api_router
from core.config import (
    LOG_LEVEL,
    LOG_FORMAT,
)

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
)

app = FastAPI(
    title="Movie Catalog",
)
app.include_router(api_router)


@app.get("/")
def read_root(request: Request, name: str = "Guest"):
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )

    return {
        "message": f"Hello {name}!",
        "docs": str(docs_url),
    }
