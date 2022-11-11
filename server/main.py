import uvicorn

from . import settings
from .di import bootstrap
from .web.app import create_app

bootstrap()

app = create_app()

if __name__ == "__main__":  # pragma: no cover
    config: dict = dict(
        host=settings.HOST,
        port=settings.PORT,
        use_colors=True,
    )

    if settings.DEBUG:
        config["reload"] = True

    uvicorn.run("server.main:app", **config)
