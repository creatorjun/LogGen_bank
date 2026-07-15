# infrastructure/network/udp_sender.py
import asyncio
from domain.ports.log_sender_port import LogSenderPort


class UdpSender(LogSenderPort):
    async def send(self, host: str, port: int, payload: bytes) -> bool:
        try:
            loop = asyncio.get_running_loop()
            transport, _ = await loop.create_datagram_endpoint(
                asyncio.DatagramProtocol,
                remote_addr=(host, port),
            )
            try:
                transport.sendto(payload)
            finally:
                transport.close()
            return True
        except OSError:
            return False
