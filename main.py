from PyProxyServer.port_forward import PortForward

if __name__ == '__main__':
    pf = PortForward("0.0.0.0", 16666, "127.0.0.1", 16667)
    pf.start()
    pf.loop()
