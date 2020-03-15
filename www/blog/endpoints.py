import logging

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from ..utils import get_display_path, is_localhost
from . import content, stat_reload

logger = logging.getLogger(__name__)


class HotReload(WebSocketEndpoint):
    encoding = "text"  # type: ignore

    async def on_connect(self, ws: WebSocket) -> None:
        if ws.url.hostname is None or not is_localhost(ws.url.hostname):
            return
        await ws.accept()

    async def on_receive(self, ws: WebSocket, message: str) -> None:
        if message != "reload:ping":
            return

        path = stat_reload.find_changed(
            str(path) for path in content.iter_content_paths()
        )

        if path is None:
            return

        message = "Detected file change in '%s'. Reloading..."
        logger.warning(message, get_display_path(path))

        await content.load_content()
        await ws.send_text("reload")
        stat_reload.reset()
