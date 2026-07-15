# tester.py
import socket
import datetime

HOST: str = "0.0.0.0"
PORT: int = 514
BUFFER: int = 65535
ENCODING: str = "euc-kr"


def main() -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))

    print(f"[UDP Tester] Listening on {HOST}:{PORT} ...")
    print("-" * 80)

    count: int = 0
    while True:
        data, addr = sock.recvfrom(BUFFER)
        count += 1
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        try:
            message = data.decode(ENCODING)
        except UnicodeDecodeError:
            message = data.decode(ENCODING, errors="replace")
        print(f"[{timestamp}] #{count:06d} from {addr[0]}:{addr[1]}")
        print(message)
        print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[UDP Tester] Stopped.")
