import uvicorn

from .web.app import create_app

app = create_app()

if __name__ == "__main__":  # pragma: no cover
    uvicorn.run("server.main:app", reload=True, use_colors=True)
