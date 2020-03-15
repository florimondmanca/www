import logging
from typing import Optional

from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from ..utils import get_display_path, is_localhost
from . import content, resources

logger = logging.getLogger(__name__)


class HotReload(WebSocketEndpoint):
    encoding = "text"  # type: ignore

    def _find_path_of_any_changed_file(self) -> Optional[str]:
        for path in map(str, resources.content_files):
            if resources.file_change_detector.has_changed(path):
                return path
        return None

    async def on_connect(self, ws: WebSocket) -> None:
        if ws.url.hostname is None or not is_localhost(ws.url.hostname):
            return
        await ws.accept()

    async def on_receive(self, ws: WebSocket, message: str) -> None:
        if message != "reload:ping":
            return

        path = self._find_path_of_any_changed_file()
        if path is None:
            return

        message = "Detected file change in '%s'. Reloading..."
        logger.warning(message, get_display_path(path))

        await content.reload()
        await ws.send_text("reload")
        resources.file_change_detector.reset()
