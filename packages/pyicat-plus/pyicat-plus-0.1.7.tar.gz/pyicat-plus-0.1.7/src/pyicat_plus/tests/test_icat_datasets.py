import pytest
import xml.etree.ElementTree as etree
from ..concurrency import Empty


def test_start_investigation(icat_metadata_client):
    client, messages = icat_metadata_client
    client.check_health()
    client.start_investigation(proposal="hg123", beamline="id00")
    message = messages.get(timeout=10)

    root = etree.fromstring(message)
    names = {child.tag.replace("{http://www.esrf.fr/icat}", "") for child in root}
    expected = {"startDate", "experiment", "instrument"}
    assert names == expected
    assert messages.empty()


def test_start_bad_investigation(icat_metadata_client):
    client, messages = icat_metadata_client
    client.check_health()
    client.start_investigation(proposal="hg666", beamline="id00")
    with pytest.raises(Empty):
        messages.get(timeout=2)


def test_send_metadata(icat_metadata_client):
    client, messages = icat_metadata_client
    client.send_metadata(
        proposal="hg123",
        beamline="id00",
        dataset="datasetname",
        path="/path-of-dataset",
        metadata={"Sample_name": "samplename", "field1": "value1", "field2": [1, 2, 3]},
    )
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


def test_send_metadata_via_file(icat_metadata_client, tmpdir):
    store_filename = tmpdir / "test.xml"

    client, messages = icat_metadata_client
    client.store_metadata(
        str(store_filename),
        proposal="hg123",
        beamline="id00",
        dataset="datasetname",
        path="/path-of-dataset",
        metadata={"Sample_name": "samplename", "field1": "value1", "field2": [1, 2, 3]},
    )

    with pytest.raises(Empty):
        message = messages.get(timeout=1)

    assert store_filename.exists()

    client.send_metadata_from_file(str(store_filename))

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


def test_send_missing_data(icat_metadata_client):
    client, messages = icat_metadata_client
    with pytest.raises(AssertionError, match="ICAT requires the beamline name"):
        client.send_metadata(
            proposal=None,
            beamline=None,
            dataset=None,
            path=None,
            metadata=None,
        )


def test_send_missing_metadata(icat_metadata_client):
    client, messages = icat_metadata_client
    with pytest.raises(
        AssertionError, match="ICAT metadata field 'Sample_name' is missing"
    ):
        client.send_metadata(
            proposal="hg123",
            beamline="id00",
            dataset="datasetname",
            path="/path-of-dataset",
            metadata={},
        )
