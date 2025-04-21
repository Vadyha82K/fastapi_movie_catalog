from fastapi import (
    Request,
)

from api.api_v1.movies.views import app


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


