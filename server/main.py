import uvicorn

from .app import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("server.main:app", reload=True, use_colors=True)
