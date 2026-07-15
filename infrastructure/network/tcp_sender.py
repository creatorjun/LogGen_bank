# infrastructure/network/tcp_sender.py
import asyncio
from domain.ports.log_sender_port import LogSenderPort


class TcpSender(LogSenderPort):
    CONNECT_TIMEOUT: float = 5.0
    SEND_TIMEOUT: float = 10.0

    async def send(self, host: str, port: int, payload: bytes) -> bool:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=self.CONNECT_TIMEOUT,
            )
            try:
                writer.write(payload)
                await asyncio.wait_for(writer.drain(), timeout=self.SEND_TIMEOUT)
                return True
            finally:
                writer.close()
                try:
                    await writer.wait_closed()
                except Exception:
                    pass
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False
        except Exception:
            return False
