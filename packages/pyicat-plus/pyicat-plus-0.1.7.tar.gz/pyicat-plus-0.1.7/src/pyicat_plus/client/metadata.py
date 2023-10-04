import os
from typing import Optional, List
import xml.etree.ElementTree as etree

from .xmlns import dataset_as_xml
from .xmlns import investigation_as_xml
from .messaging import IcatMessagingClient
from . import defaults


class IcatMetadataClient:
    """Client for storing dataset metadata in ICAT."""

    def __init__(
        self,
        queue_urls: Optional[List[str]] = None,
        queue_name: Optional[str] = None,
        monitor_port: Optional[int] = None,
        timeout: Optional[float] = None,
    ):
        if queue_urls is None:
            defaults.METADATA_BROKERS
        if queue_name is None:
            queue_name = defaults.METADATA_QUEUE
        self._client = IcatMessagingClient(
            queue_urls, queue_name, monitor_port=monitor_port, timeout=timeout
        )

    def send_metadata(
        self,
        beamline: str,
        proposal: str,
        dataset: str,
        path: str,
        metadata: dict,
    ):
        root = dataset_as_xml(
            beamline=beamline,
            proposal=proposal,
            dataset=dataset,
            path=path,
            metadata=metadata,
        )
        self._client.send(etree.tostring(root))

    def store_metadata(
        self,
        filename: str,
        beamline: str,
        proposal: str,
        dataset: str,
        path: str,
        metadata: dict,
    ):
        root = dataset_as_xml(
            beamline=beamline,
            proposal=proposal,
            dataset=dataset,
            path=path,
            metadata=metadata,
        )
        filename, ext = os.path.splitext(filename)
        if not ext:
            ext = ".xml"
        filename += ext
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "wb") as f:
            f.write(etree.tostring(root))

    def send_metadata_from_file(self, filename: str):
        filename, ext = os.path.splitext(filename)
        if not ext:
            ext = ".xml"
        filename += ext
        with open(filename, "rb") as f:
            payload = f.read()
        self._client.send(payload)

    def start_investigation(self, beamline: str, proposal: str, start_datetime=None):
        root = investigation_as_xml(
            beamline=beamline, proposal=proposal, start_datetime=start_datetime
        )
        self._client.reconnect()
        self._client.send(etree.tostring(root))

    def check_health(self):
        """Raises an exception when not healthy"""
        self._client.check_health()
