import socket
import threading


def socket_thread(host, port, conn: socket.socket, addr):
    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    sock.connect((host, port))
    pp = conn.recv(4096)
    print(*addr, "REQ ", pp)

    sock.send(pp)
    try:
        dd = sock.recv(4096)
    except TimeoutError:
        sock.shutdown(1)
        sock.close()
        conn.shutdown(1)
        conn.close()
        return
    except ConnectionResetError as e:
        print(*addr, "RESET", e)
        sock.shutdown()
        sock.close()
        conn.shutdown(1)
        conn.close()
        return
    conn.send(dd)
    print(*addr, "RESP", dd)
    while dd:
        try:
            dd = sock.recv(4096)
            conn.send(dd)
            print(*addr, "RESP", dd)
        except TimeoutError:
            break
        except ConnectionResetError as e:
            print(*addr, "RESET", e)
            sock.shutdown(1)
            sock.close()
            conn.shutdown(1)
            conn.close()
            return
    print(*addr, "OVER")

    sock.shutdown(1)
    sock.close()
    conn.shutdown(1)
    conn.close()


class PortForward:
    def __init__(self, listen_host, listen_port, conn_host, conn_port) -> None:
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.conn_host = conn_host
        self.conn_port = conn_port

        self.sock_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock_listen.bind((self.listen_host, self.listen_port))

    @classmethod
    def from_configs(cls, config_file: str):
        import configparser
        cp = configparser.ConfigParser()
        cp.read(config_file)
        return cls(listen_host=cp.get("listen", "host"), listen_port=int(cp.get("listen", "port")),
                   conn_host=cp.get("connection", "host"), conn_port=int(cp.get("connection", "port")))

    def start(self):
        self.sock_listen.listen()

    def close(self):
        print("SOCKET HANDLE", *self.sock_listen.getsockname(), "CLOSED.")
        self.sock_listen.shutdown(1)
        self.sock_listen.close()

    def loop(self):
        while True:
            try:
                conn, addr = self.sock_listen.accept()
            except KeyboardInterrupt:
                break

            # threading
            threading.Thread(target=socket_thread, args=[self.conn_host, self.conn_port, conn, addr]).start()
            # blocking
            # socket_thread(self.conn_host, self.conn_port, conn, addr)
            print(*addr, "**RECV**")
        self.close()
