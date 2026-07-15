# application/services/log_file_writer.py
import asyncio
from datetime import datetime
from pathlib import Path


class LogFileWriter:
    LOG_DIR: str = "logs"
    ENCODING: str = "euc-kr"

    def __init__(self) -> None:
        self._path: Path | None = None
        self._lock = asyncio.Lock()

    def open_session(self) -> None:
        log_dir = Path(self.LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self._path = log_dir / f"loggen_{timestamp}.txt"

    def close_session(self) -> None:
        self._path = None

    async def write(self, raw_log: str) -> None:
        if self._path is None:
            return
        async with self._lock:
            with self._path.open("a", encoding=self.ENCODING, errors="replace") as f:
                f.write(raw_log + "\n")
