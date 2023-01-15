import uvicorn
import uvicorn.supervisors

from . import settings
from .di import bootstrap
from .web.app import create_app

bootstrap()

app = create_app()


def get_config() -> uvicorn.Config:
    config: dict = dict(
        host=settings.HOST,
        port=settings.PORT,
        use_colors=True,
        reload=settings.DEBUG,
    )

    return uvicorn.Config("server.main:app", **config)


if __name__ == "__main__":  # pragma: no cover
    config = get_config()
    server = uvicorn.Server(config)

    if config.should_reload:
        sock = config.bind_socket()
        uvicorn.supervisors.ChangeReload(
            config, target=server.run, sockets=[sock]
        ).run()
    else:
        server.run()
