import os
from datetime import datetime
from typing import Optional, List
from urllib.parse import urljoin
import requests
import numpy
import logging

from ..concurrency.query_pool import QueryPool
from .interface import DatasetId
from ..utils.maxsizedict import MaxSizeDict
from ..utils.url import normalize_url
from . import defaults

logger = logging.getLogger(__name__)


def arg_smallest_positive(arr: numpy.ndarray) -> Optional[int]:
    condition = arr >= 0
    if condition.any():
        return numpy.where(condition, arr, numpy.inf).argmin()


class IcatInvestigationClient:
    """Client for the investigation part of the ICAT+ REST API.

    An "investigation" is a time slot assigned to a particular proposal
    at a particular beamline.

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
    ):
        if api_key is None:
            api_key = defaults.ELOGBOOK_TOKEN
        url = normalize_url(url, default_scheme=self.DEFAULT_SCHEME)

        path = f"dataacquisition/{api_key}/investigation"
        query = (
            "?instrumentName={beamline}&investigationName={proposal}&sortBy=startdate"
        )
        self._investigation_url = urljoin(url, path + query)

        path = f"dataacquisition/{api_key}/dataset"
        query = "?investigationId={investigation_id}"
        self._dataset_url = urljoin(url, path + query)

        self.raise_error = False
        self.__query_pool = QueryPool(timeout=timeout, maxqueries=20)
        self.__investigation_info = MaxSizeDict(maxsize=20)

    @property
    def timeout(self):
        return self.__query_pool.timeout

    @timeout.setter
    def timeout(self, value: Optional[float] = None):
        self.__query_pool.timeout = value

    def _get_with_response_parsing(
        self, url: str, timeout: Optional[float] = None
    ) -> Optional[list]:
        """Return `None` means the information is not available at this moment.
        An empty list means that an error has occured or an actual empty list
        is returned.
        """
        try:
            response = self.__query_pool.execute(
                requests.get, args=(url,), timeout=timeout, default=None
            )
        except requests.exceptions.ReadTimeout:
            return None
        except Exception as e:
            if self.raise_error:
                raise
            logger.exception(e)
            return None
        if response is None:
            return None
        if self.raise_error:
            response.raise_for_status()
        elif not response.ok:
            logger.error("%s: %s", response, response.text)
        if response.ok:
            return response.json()
        else:
            return list()

    def investigation_info(
        self, beamline: str, proposal: str, timeout: Optional[float] = None
    ) -> Optional[dict]:
        investigation_key = beamline, proposal
        ninfo = self.__investigation_info.get(investigation_key)
        if ninfo is not None:
            return ninfo

        # Get all investigations for this proposal and beamline
        url = self._investigation_url.format(beamline=beamline, proposal=proposal)
        investigations = self._get_with_response_parsing(url, timeout=timeout)
        if investigations is None:
            return None  # not available at the moment
        if not investigations:
            return dict()  # error or no investigation found

        # Get the closest investigation which started before "now".
        # If there is no such investigation, get the closest investigation
        # which starts after "time".
        now = datetime.now().astimezone()
        seconds_since_start = list()
        for i, info in enumerate(investigations):
            startdate = info.get("startDate")
            if startdate:
                dt = datetime.fromisoformat(startdate)
            else:
                dt = datetime.utcfromtimestamp(i).astimezone()
            seconds_since_start.append((now - dt).total_seconds())
        seconds_since_start = numpy.array(seconds_since_start)
        idx = arg_smallest_positive(seconds_since_start)
        if idx is None:
            idx = arg_smallest_positive(-seconds_since_start)
        info = investigations[idx]

        # Normalize information
        for key in ["parameters", "visitId"]:
            info.pop(key, None)
        ninfo = dict()
        ninfo["proposal"] = info.pop("name", None)
        ninfo["beamline"] = info.pop("instrument", dict()).get("name", None)
        ninfo.update(info)
        ninfo["e-logbook"] = f"https://data.esrf.fr/investigation/{info['id']}/events"
        ninfo[
            "data portal"
        ] = f"https://data.esrf.fr/investigation/{info['id']}/datasets"

        self.__investigation_info[investigation_key] = ninfo
        return ninfo

    def _investigation_id(
        self, beamline: str, proposal: str, timeout: Optional[float] = None
    ) -> Optional[int]:
        info = self.investigation_info(
            beamline=beamline, proposal=proposal, timeout=timeout
        )
        if info is None:
            return None
        return info.get("id", None)

    def registered_dataset_ids(
        self, beamline: str, proposal: str, timeout: Optional[float] = None
    ) -> Optional[List[DatasetId]]:
        investigation_id = self._investigation_id(
            beamline=beamline, proposal=proposal, timeout=timeout
        )
        if investigation_id is None:
            return None
        url = self._dataset_url.format(investigation_id=investigation_id)
        datasets = self._get_with_response_parsing(url, timeout=timeout)
        if datasets is None:
            return None
        return [self._icat_dataset_to_datasetid(dataset) for dataset in datasets]

    @staticmethod
    def _icat_dataset_to_datasetid(dataset: dict) -> DatasetId:
        location = dataset["location"]
        location, name = os.path.split(location)
        while location and not name:
            location, name = os.path.split(location)
        return DatasetId(name=name, path=dataset["location"])
