from enum import Enum
from datetime import datetime
import requests
import base64
import mimetypes
import socket
from urllib.parse import urljoin
from typing import Optional, Iterable, List
import logging

from ..utils.url import normalize_url
from .. import __version__
from . import defaults

logger = logging.getLogger(__name__)

MessageCategory = Enum("MessageCategory", "debug info error commandLine comment")
MessageType = Enum("MessageType", "annotation notification")

MessageCategoryMapping = {
    "debug": MessageCategory.debug,
    "info": MessageCategory.info,
    "warning": MessageCategory.error,
    "warn": MessageCategory.error,
    "error": MessageCategory.error,
    "critical": MessageCategory.error,
    "fatal": MessageCategory.error,
    "command": MessageCategory.commandLine,
    "comment": MessageCategory.comment,
}

MessageTypeMapping = {
    MessageCategory.debug: MessageType.notification,
    MessageCategory.info: MessageType.notification,
    MessageCategory.error: MessageType.notification,
    MessageCategory.commandLine: MessageType.notification,
    MessageCategory.comment: MessageType.annotation,
}


class IcatElogbookClient:
    """Client for the e-logbook part of the ICAT+ REST API.

    REST API docs:
    https://icatplus.esrf.fr/api-docs/

    The ICAT+ server project:
    https://gitlab.esrf.fr/icat/icat-plus/-/blob/master/README.md
    """

    DEFAULT_SCHEME = "https"

    def __init__(
        self,
        url: str,
        api_key: Optional[str] = None,
        timeout: Optional[float] = None,
        **payload,
    ):
        if api_key is None:
            api_key = defaults.ELOGBOOK_TOKEN
        url = normalize_url(url, default_scheme=self.DEFAULT_SCHEME)

        path = f"dataacquisition/{api_key}/notification"
        self._message_url = urljoin(url, path)

        path = f"dataacquisition/{api_key}/base64"
        self._data_url = urljoin(url, path)

        self._init_payload = payload
        self._init_payload.setdefault("machine", socket.getfqdn())
        self._init_payload.setdefault("software", "pyicat-plus_v" + __version__)

        self.raise_error = True
        if timeout is None:
            timeout = 0.1
        self.timeout = timeout

    def _merge_payloads(self, message_payload: dict, call_payload: dict) -> dict:
        payloads = self._sorted_payloads(message_payload, call_payload)
        result = {k: v for payload in payloads for k, v in payload.items()}
        tags = self._merge_payload_tags(*payloads)
        if tags:
            result.pop("tags", None)
            result["tag"] = tags
        return result

    def _sorted_payloads(self, message_payload: dict, call_payload: dict) -> List[dict]:
        """Sorted by increasing priority"""
        return [message_payload, self._init_payload, call_payload]

    def _merge_payload_tags(self, *payloads: Iterable[dict]) -> List[dict]:
        """The payload tags can be eithers a list of strings or a list of dictionaries.
        The return value are the merged tags as a list of dictionaries.
        """
        names = set()
        tags = list()
        for payload in payloads:
            ptags = payload.get("tag", list()) + payload.get("tags", list())
            for tag in ptags:
                if isinstance(tag, str):
                    if tag in names:
                        continue
                    names.add(tag)
                    tags.append({"name": tag})
                else:
                    if tag["name"] in names:
                        continue
                    names.add(tag["name"])
                    tags.append(tag)
        return tags

    def _post_with_payload(
        self, url: str, message_payload: dict, call_payload: dict
    ) -> None:
        payload = self._merge_payloads(message_payload, call_payload)
        payload.setdefault("creationDate", datetime.now().isoformat())
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
        except requests.exceptions.ReadTimeout:
            return  # we have no confirmation that the call succeeded
        except Exception as e:
            if self.raise_error:
                raise
            logger.exception(e)
            return
        if self.raise_error:
            response.raise_for_status()
        elif not response.ok:
            logger.error("%s: %s", response, response.text)

    def send_message(
        self,
        message: str,
        category: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        **call_payload,
    ):
        url = self._compose_url(
            url=self._message_url, beamline=beamline, proposal=proposal
        )
        message_payload = self._encode_message(message, category, dataset=dataset)
        self._post_with_payload(url, message_payload, call_payload)

    def send_binary_data(
        self,
        data: bytes,
        mimetype: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        **call_payload,
    ):
        url = self._compose_url(
            url=self._data_url, beamline=beamline, proposal=proposal
        )
        message_payload = self._encode_binary_data(data, mimetype=mimetype)
        self._post_with_payload(url, message_payload, call_payload)

    @staticmethod
    def _compose_url(
        url: str, beamline: Optional[str] = None, proposal: Optional[str] = None
    ):
        query = {}
        if beamline:
            query["instrumentName"] = beamline
        if proposal:
            query["investigationName"] = proposal
        query = "&".join([f"{k}={v}" for k, v in query.items()])
        return f"{url}?{query}"

    def send_text_file(
        self,
        filename: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        **payload,
    ):
        with open(filename, "r") as f:
            message = f.read()
        self.send_message(
            message,
            category="comment",
            proposal=proposal,
            beamline=beamline,
            dataset=dataset,
            **payload,
        )

    def send_binary_file(
        self,
        filename: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        **payload,
    ):
        with open(filename, "rb") as f:
            data = f.read()
        mimetype, _ = mimetypes.guess_type(filename, strict=True)
        self.send_binary_data(
            data, mimetype=mimetype, beamline=beamline, proposal=proposal, **payload
        )

    def _encode_message(
        self,
        message: str,
        category: str,
        dataset: Optional[str] = None,
    ) -> dict:
        try:
            category = MessageCategoryMapping[category.lower()]
        except KeyError:
            raise ValueError(category, "Not a valid e-logbook category") from None
        message_type = MessageTypeMapping[category]
        message = {
            "type": message_type.name,
            "category": category.name,
            "content": [{"format": "plainText", "text": message}],
        }
        if dataset:
            message["datasetName"] = dataset
        return message

    def _encode_binary_data(
        self,
        data: bytes,
        mimetype: Optional[str] = None,
    ) -> dict:
        if not mimetype:
            # arbitrary binary data
            mimetype = "application/octet-stream"
        data_header = f"data:{mimetype};base64,"
        data_blob = base64.b64encode(data).decode("latin-1")
        return {"base64": data_header + data_blob}
