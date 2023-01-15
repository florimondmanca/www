import threading
import time
from contextlib import contextmanager
from typing import Iterator

import uvicorn


class Server(uvicorn.Server):
    url = "http://localhost:8000"

    def install_signal_handlers(self) -> None:
        pass

    @contextmanager
    def run_in_thread(self) -> Iterator[None]:
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()
