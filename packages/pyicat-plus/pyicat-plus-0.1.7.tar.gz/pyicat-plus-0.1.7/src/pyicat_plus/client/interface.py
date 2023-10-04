from typing import Optional, List, Tuple, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetId:
    name: str
    path: str


class IcatClientInterface:
    def send_message(
        self,
        msg: str,
        msg_type="comment",
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload
    ):
        raise NotImplementedError

    def send_data(
        self,
        data: bytes,
        mimetype: Optional[str] = None,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload
    ):
        raise NotImplementedError

    def send_text_file(
        self,
        filename: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload
    ):
        raise NotImplementedError

    def send_binary_file(
        self,
        filename: str,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        beamline_only: Optional[bool] = None,
        **payload
    ):
        raise NotImplementedError

    def start_investigation(
        self,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        start_datetime=None,
    ):
        raise NotImplementedError

    def store_dataset(
        self,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        path: Optional[str] = None,
        metadata: dict = None,
        store_filename: Optional[str] = None,
    ):
        raise NotImplementedError

    def store_processed_dataset(
        self,
        beamline: Optional[str] = None,
        proposal: Optional[str] = None,
        dataset: Optional[str] = None,
        path: Optional[str] = None,
        metadata: dict = None,
        raw: Sequence = tuple(),
        store_filename: Optional[str] = None,
    ):
        raise NotImplementedError

    def store_dataset_from_file(self, store_filename: Optional[str] = None):
        raise NotImplementedError

    def investigation_info(
        self, beamline: str, proposal: str, timeout: Optional[float] = None
    ) -> Optional[dict]:
        raise NotImplementedError

    def registered_dataset_ids(
        self, beamline: str, proposal: str
    ) -> Optional[List[DatasetId]]:
        raise NotImplementedError

    def investigation_info_string(
        self, beamline: str, proposal: str, timeout: Optional[float] = None
    ) -> str:
        raise NotImplementedError

    def investigation_summary(
        self, beamline: str, proposal: str, timeout: Optional[float] = None
    ) -> List[Tuple]:
        raise NotImplementedError

    @property
    def expire_datasets_on_close(self) -> bool:
        raise NotImplementedError

    @property
    def reason_for_missing_information(self) -> str:
        raise NotImplementedError
