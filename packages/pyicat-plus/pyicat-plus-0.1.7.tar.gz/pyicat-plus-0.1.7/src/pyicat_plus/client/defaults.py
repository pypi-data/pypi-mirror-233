from typing import List

ELOGBOOK_TOKEN: str = "elogbook-00000000-0000-0000-0000-000000000000"

METADATA_QUEUE: str = "icatIngest"
METADATA_BROKERS: List[str] = ["bcu-mq-01.esrf.fr:61613", "bcu-mq-02.esrf.fr:61613"]

ARCHIVE_QUEUE: str = "icatArchiveRestoreStatus"
ARCHIVE_BROKERS: List[str] = ["bcu-mq-01.esrf.fr:61613", "bcu-mq-02.esrf.fr:61613"]
