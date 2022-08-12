import socket
import threading

def socket_thread(host,port,conn,addr):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((host,port))
    sock.



class PortForward:
    def __init__(self, listen_host, listen_port, conn_host, conn_port) -> None:
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.conn_host = conn_host
        self.conn_port = conn_port

        self.sock_listen = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    def start(self):
        self.sock_listen.listen()


    def loop(self):
        while True:
            conn,addr = self.sock_listen.accept()
