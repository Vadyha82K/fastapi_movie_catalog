from fastapi import (
    FastAPI,
    Request,
)

from api import router as api_router


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
