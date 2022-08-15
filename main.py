import argparse

from PyProxyServer.port_forward import PortForward


def parse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cfg", type=str, required=False,
                        help=".cfg file if used by static commands, used only if required.")
    parser.add_argument("--host", type=str, required=False, help="host address to listen")
    parser.add_argument("--port", type=int, required=False, help="port to listen")
    parser.add_argument("--conn-host", type=str, required=False, help="the host address to connect")
    parser.add_argument("--conn-port", type=str, required=False, help="the host port to connect")
    return parser


def main():
    parser = parse()
    args: argparse.Namespace = parser.parse_args()

    if args.cfg:
        pf = PortForward.from_configs("./default.cfg")
        pf.start()
        pf.loop()
        return
    elif args.host and args.port and args.conn_host and args.conn_port:
        print({'listen': {'host': args.host, 'port': args.port},
               'connection': {'host': args.conn_host, 'port': args.conn_port}})
        pf = PortForward(args.host, args.port, args.conn_host, args.conn_port)
        pf.start()
        pf.loop()
        return
    else:
        print("argument fail with:", args.__dict__)
        parser.print_help()
        return


if __name__ == '__main__':
    main()
