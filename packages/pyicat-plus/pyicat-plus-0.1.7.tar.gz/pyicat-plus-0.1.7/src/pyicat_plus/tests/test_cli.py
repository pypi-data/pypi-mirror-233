import xml.etree.ElementTree as etree
from ..apps import store_raw
from ..apps import store_processed


def test_store_raw(icat_metadata_client, icat_backend):
    _, messages = icat_metadata_client

    argv = [
        "",
        "--beamline",
        "id00",
        "--proposal",
        "hg123",
        "--dataset",
        "datasetname",
        "--path",
        "/path/of/dataset",
        "--sample",
        "samplename",
        "-p",
        "field1=value1",
        "-p",
        "field2=[1, 2, 3]",
        "--queue",
        icat_backend["metadata_urls"][0],
    ]
    store_raw.main(argv)

    message = messages.get(timeout=10)

    root = etree.fromstring(message)
    names = {child.tag.replace("{http://www.esrf.fr/icat}", "") for child in root}
    expected = {
        "endDate",
        "location",
        "startDate",
        "parameter",
        "sample",
        "investigation",
        "instrument",
        "name",
    }
    assert names == expected
    assert messages.empty()


def test_store_processed(icat_metadata_client, icat_backend):
    _, messages = icat_metadata_client

    argv = [
        "",
        "--beamline",
        "id00",
        "--proposal",
        "hg123",
        "--dataset",
        "datasetname",
        "--path",
        "/path/of/processed",
        "--sample",
        "samplename",
        "-p",
        "field1=value1",
        "-p",
        "field2=[1, 2, 3]",
        "--queue",
        icat_backend["metadata_urls"][0],
        "--raw",
        "/path/of/dataset1",
        "--raw",
        "/path/of/dataset2",
    ]
    store_processed.main(argv)

    message = messages.get(timeout=10)

    root = etree.fromstring(message)
    names = {child.tag.replace("{http://www.esrf.fr/icat}", "") for child in root}
    expected = {
        "endDate",
        "location",
        "startDate",
        "parameter",
        "sample",
        "investigation",
        "instrument",
        "name",
    }
    assert names == expected
    assert messages.empty()
