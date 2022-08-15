from PyProxyServer.port_forward import PortForward

if __name__ == '__main__':
    pf = PortForward.from_configs("./default.cfg")
    pf.start()
    pf.loop()
    # pf = PortForward("0.0.0.0", 16666, "localhost", 6379)
    # pf.start()
    # pf.loop()
