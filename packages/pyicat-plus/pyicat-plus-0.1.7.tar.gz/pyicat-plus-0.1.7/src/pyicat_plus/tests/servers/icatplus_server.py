import os
import re
import socket
import json
import http.server
import logging
from datetime import datetime

from pyicat_plus.tests.servers.utils import ReuseAddrTCPServer
from pyicat_plus.tests.servers.utils import basic_config

logger = logging.getLogger("ICATPLUS SERVER")
basic_config(
    logger=logger,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class MyTCPRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, s_out=None, icat_data_dir=None, **kw):
        self.s_out = s_out
        self.icat_data_dir = icat_data_dir
        self._investigation_id = 1234
        self._investigation_startdate = datetime.now().astimezone().isoformat()
        super().__init__(*args, **kw)

    def do_HEAD(self):
        logger.info("HEAD")
        self.reply_ok()

    def do_GET(self):
        if self._handle_investigation():
            return
        if self._handle_dataset():
            return
        logger.error("Bad GET request: %s", self.path)
        self.reply_bad_request()

    def do_POST(self):
        if self._handle_elogbook_message():
            return
        if self._handle_elogbook_data():
            return
        if self._handle_elogbook_message_beamline_only():
            return
        if self._handle_elogbook_message_no_beamline():
            return
        if self._handle_elogbook_data_beamline_only():
            return
        logger.error("Bad POST request: %s", self.path)
        self.reply_bad_request()

    def _handle_investigation(self):
        fmt = "/dataacquisition/(?P<apikey>[^//]+)/investigation\\?instrumentName=(?P<instrument>[^//]+)&investigationName=(?P<investigation>[^//]+)&sortBy=startdate"
        mresult = re.match(fmt, self.path)
        if not mresult:
            return
        if "666" in mresult.groupdict()["investigation"]:
            self.reply_error()
            return True
        response = [
            {"id": self._investigation_id, "startDate": self._investigation_startdate}
        ]
        logger.info("Investigation GET response: %s", response)
        self.reply_json(response)
        return True

    def _handle_dataset(self):
        fmt = f"/dataacquisition/(?P<apikey>[^//]+)/dataset\\?investigationId={self._investigation_id}"
        mresult = re.match(fmt, self.path)
        if not mresult:
            return
        datasets = list()
        if self.icat_data_dir:
            for name in os.listdir(self.icat_data_dir):
                filename = os.path.join(self.icat_data_dir, name)
                with open(filename, "r") as content:
                    datasets.append(json.load(content))
        logger.info("Dataset GET response: %s", datasets)
        self.reply_json(datasets)
        return True

    def _handle_elogbook_message(self):
        logger.info(self.path)
        fmt = "/dataacquisition/(?P<apikey>[^//]+)/notification\\?instrumentName=(?P<instrument>[^//]+)&investigationName=(?P<investigation>[^//]+)"
        mresult = re.match(fmt, self.path)
        if not mresult:
            return
        if (
            self.headers.get("content-type") != "application/json"
            or "666" in mresult.groupdict()["investigation"]
        ):
            self.reply_bad_request()
            return True
        length = int(self.headers.get("content-length"))
        adict = json.loads(self.rfile.read(length))
        adict.update(mresult.groupdict())
        self.on_elog_message(adict)
        self.reply_ok()
        return True

    def _handle_elogbook_data(self):
        fmt = "/dataacquisition/(?P<apikey>[^//]+)/base64\\?instrumentName=(?P<instrument>[^//]+)&investigationName=(?P<investigation>[^//]+)"
        mresult = re.match(fmt, self.path)
        if not mresult:
            return
        if (
            self.headers.get("content-type") != "application/json"
            or "666" in mresult.groupdict()["investigation"]
        ):
            self.reply_bad_request()
            return True
        length = int(self.headers.get("content-length"))
        adict = json.loads(self.rfile.read(length))
        adict.update(mresult.groupdict())
        self.on_elog_message(adict)
        self.reply_ok()
        return True

    def _handle_elogbook_message_beamline_only(self):
        logger.info(self.path)
        fmt = "/dataacquisition/(?P<apikey>[^//]+)/notification\\?instrumentName=(?P<instrument>[^//]+)"
        mresult = re.match(fmt, self.path)
        if not mresult:
            return
        if self.headers.get("content-type") != "application/json":
            self.reply_bad_request()
            return True
        length = int(self.headers.get("content-length"))
        adict = json.loads(self.rfile.read(length))
        adict.update(mresult.groupdict())
        self.on_elog_message(adict)
        self.reply_ok()
        return True

    def _handle_elogbook_message_no_beamline(self):
        logger.info(self.path)
        fmt = "/dataacquisition/(?P<apikey>[^//]+)/notification"
        mresult = re.match(fmt, self.path)
        if not mresult:
            return
        if self.headers.get("content-type") != "application/json":
            self.reply_bad_request()
            return True
        length = int(self.headers.get("content-length"))
        adict = json.loads(self.rfile.read(length))
        adict.update(mresult.groupdict())
        self.on_elog_message(adict)
        self.reply_ok()
        return True

    def _handle_elogbook_data_beamline_only(self):
        fmt = "/dataacquisition/(?P<apikey>[^//]+)/base64\\?instrumentName=(?P<instrument>[^//]+)"
        mresult = re.match(fmt, self.path)
        if not mresult:
            return
        if self.headers.get("content-type") != "application/json":
            self.reply_bad_request()
            return True
        length = int(self.headers.get("content-length"))
        adict = json.loads(self.rfile.read(length))
        adict.update(mresult.groupdict())
        self.on_elog_message(adict)
        self.reply_ok()
        return True

    def reply_ok(self):
        self.send_response(http.HTTPStatus.OK)
        self.end_headers()

    def reply_bad_request(self):
        self.send_response(http.HTTPStatus.BAD_REQUEST)
        self.end_headers()

    def reply_not_found(self):
        self.send_response(http.HTTPStatus.NOT_FOUND)
        self.end_headers()

    def reply_error(self):
        self.send_response(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        self.end_headers()

    def reply_json(self, adict):
        body = json.dumps(adict).encode()
        self.send_response(http.HTTPStatus.OK)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def on_elog_message(self, adict):
        if not adict:
            return
        logger.info("received message:\n %s", adict)
        if self.s_out is not None:
            self.s_out.sendall(json.dumps(adict).encode() + b"\n")


def main(port=8443, port_out=0, icat_data_dir=None):
    if port_out:
        s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_out.connect(("localhost", port_out))
    else:
        s_out = None

    class MyTCPRequestHandlerWithSocket(MyTCPRequestHandler):
        def __init__(self, *args, **kw):
            super().__init__(*args, s_out=s_out, icat_data_dir=icat_data_dir, **kw)

    # Create a TCP Server instance
    aServer = ReuseAddrTCPServer(("localhost", port), MyTCPRequestHandlerWithSocket)

    # Start accepting requests and setup output socket
    if port_out:
        logger.info(f"Redirect received messages to port {port_out}")
        s_out.sendall(json.dumps({"STATUS": "LISTENING"}).encode() + b"\n")
    try:
        logger.info("CTRL-C to stop")
        aServer.serve_forever()
    finally:
        logger.info("Exit.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ICAT plus server")
    parser.add_argument("--port", default=8443, type=int, help="server port")
    parser.add_argument("--port_out", default=0, type=int, help="output socket")
    parser.add_argument(
        "--icat_data_dir", default="", type=str, help="One file per dataset"
    )
    args = parser.parse_args()
    main(port=args.port, port_out=args.port_out, icat_data_dir=args.icat_data_dir)
