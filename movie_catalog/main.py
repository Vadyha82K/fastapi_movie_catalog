from fastapi import (
    FastAPI,
    Request,
)

app = FastAPI(title="Movie Catalog")


@app.get("/")
def read_root(request: Request, name: str = "Guest") -> dict:
    docs_url = request.url.replace(
        path="/docs",
        query="",
    )

    return {
        "message": f"Hello {name}!",
        "docs": docs_url,
    }
