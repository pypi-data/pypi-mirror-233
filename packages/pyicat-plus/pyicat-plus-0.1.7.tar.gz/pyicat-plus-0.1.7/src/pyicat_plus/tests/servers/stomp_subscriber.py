import os
import re
import json
import stomp
import socket
import logging
import threading

from pyicat_plus.tests.servers.utils import basic_config

logger = logging.getLogger("STOMP SUBSCRIBER")
basic_config(
    logger=logger,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn, icat_data_dir=""):
        self.conn = conn
        self.s_out = None
        self.icat_data_dir = icat_data_dir
        super().__init__()

    def redirect_messages(self, port):
        if self.s_out is not None:
            self.s_out.close()
        self.s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_out.connect(("localhost", port))
        logger.info(f"Redirect received messages to port {port}")

    def on_message(self, frame):
        message = frame.body
        header = frame.headers
        if header.get("destination") not in [
            "/queue/icatIngest",
            "/queue/icatArchiveRestoreStatus",
        ]:
            return
        logger.info(f"received message:\n {message}")

        invalid_proposal = re.findall(
            "<tns:experiment>([^<>]*666[^<>]*)<\\/tns:experiment>", message
        ) or re.findall(
            "<tns:investigation>([^<>]*666[^<>]*)<\\/tns:investigation>", message
        )
        if invalid_proposal:
            logger.info(
                "Do not register message for invalid proposal '%s'", invalid_proposal[0]
            )
            return

        if self.s_out is not None:
            self.s_out.sendall(message.encode() + b"\n")

        filename = None
        if self.icat_data_dir:
            fmt = r"\<tns\:location\>(?P<location>.+?)\<\/tns\:location\>"
            results = re.findall(fmt, message)
            if results:
                info = {"location": results[0]}
                name = "{:04d}.json".format(len(os.listdir(self.icat_data_dir)))
                filename = os.path.join(self.icat_data_dir, name)
                with open(filename, "w") as f:
                    json.dump(info, f)
        logger.info(f"dataset file saved: {filename}")


def main(host=None, port=60001, queue=None, port_out=0, icat_data_dir=""):
    if not host:
        host = "localhost"
    if not queue:
        queue = "/queue/icatIngest"
    conn = stomp.Connection([(host, port)])
    # Listener will run in a different thread
    listener = MyListener(conn, icat_data_dir)
    conn.set_listener("", listener)
    conn.connect("guest", "guest", wait=True)
    conn.subscribe(destination=queue, id=1, ack="auto")
    logger.info(f"subscribed to {queue} on STOMP {host}:{port}")
    if port_out:
        listener.redirect_messages(port_out)
        listener.s_out.sendall(b"LISTENING\n")
    logger.info("CTRL-C to stop")
    try:
        threading.Event().wait()
    finally:
        logger.info("Exit.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="STOMP client which subscribes to a STOMP queue and redirect its output to a socket"
    )
    parser.add_argument(
        "--host", default="localhost", type=str, help="STOMP server host"
    )
    parser.add_argument("--port", default=60001, type=int, help="STOMP server port")
    parser.add_argument(
        "--queue", default="/queue/icatIngest", type=str, help="STOMP queue"
    )
    parser.add_argument("--port_out", default=0, type=int, help="output socket")
    parser.add_argument(
        "--icat_data_dir", default="", type=str, help="Dataset directory"
    )
    args = parser.parse_args()

    main(
        host=args.host,
        port=args.port,
        port_out=args.port_out,
        queue=args.queue,
        icat_data_dir=args.icat_data_dir,
    )
