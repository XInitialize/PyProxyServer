import socket


def socket_thread(host, port, conn: socket.socket, addr):
    sock: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    pp = conn.recv(4096)
    print(*addr, "REQ", pp)
    sock.send(pp)
    dd = sock.recv(4096)
    conn.send(dd)
    print(*addr, "RESP", dd)
    while dd:
        dd = sock.recv(4096)
        conn.send(dd)
        print(*addr, "RESP", dd)
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

    def start(self):
        self.sock_listen.listen()

    def loop(self):
        while True:
            conn, addr = self.sock_listen.accept()
            # threading.Thread(target=socket_thread, args=[self.conn_host, self.conn_port, conn, addr]).start()
            socket_thread(self.conn_host, self.conn_port, conn, addr)
            print("**started**")
