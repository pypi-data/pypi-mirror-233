import pytest
import base64


def test_elogbook_message_wrong_category(elogbook_client):
    client, messages = elogbook_client
    with pytest.raises(ValueError):
        client.send_message(
            "mycontent",
            category="wrongcategory",
            beamline="id00",
            proposal="hg123",
            dataset="datasetname",
        )
    assert messages.empty()


def test_elogbook_message(elogbook_client):
    client, messages = elogbook_client
    client.send_message(
        "mycontent",
        category="comment",
        beamline="id00",
        proposal="hg123",
        dataset="datasetname",
    )
    message = messages.get(timeout=10)
    assert message.pop("apikey")
    assert message.pop("creationDate")
    assert message.pop("machine")
    assert message.pop("software").startswith("pyicat-plus")
    expected = {
        "type": "annotation",
        "datasetName": "datasetname",
        "category": "comment",
        "content": [{"format": "plainText", "text": "mycontent"}],
        "investigation": "hg123",
        "instrument": "id00",
    }
    assert message == expected
    assert messages.empty()


def test_ebs_elogbook_message(elogbook_ebs_client):
    client, messages = elogbook_ebs_client

    client.send_message("mycontent", category="error")
    message = messages.get(timeout=10)
    assert message.pop("apikey")
    assert message.pop("creationDate")
    assert message.pop("machine")
    expected = {
        "type": "broadcast",
        "source": "ebs",
        "category": "error",
        "software": "testsoft",
        "tag": [{"name": "testtag"}, {"name": "machine"}],
        "content": [{"format": "plainText", "text": "mycontent"}],
    }
    assert message == expected

    client.send_message(
        "mycontent", category="comment", tags=["commenttag"], software="mysoft"
    )
    message = messages.get(timeout=10)
    assert message.pop("apikey")
    assert message.pop("creationDate")
    assert message.pop("machine")
    expected = {
        "type": "broadcast",
        "source": "ebs",
        "category": "comment",
        "software": "mysoft",
        "tag": [{"name": "testtag"}, {"name": "machine"}, {"name": "commenttag"}],
        "content": [{"format": "plainText", "text": "mycontent"}],
    }
    assert message == expected

    assert messages.empty()


def test_elogbook_message_beamline_only(elogbook_client):
    client, messages = elogbook_client
    client.send_message("mycontent", category="comment", beamline="id00")
    message = messages.get(timeout=10)
    assert message.pop("apikey")
    assert message.pop("creationDate")
    assert message.pop("machine")
    assert message.pop("software").startswith("pyicat-plus")
    expected = {
        "type": "annotation",
        "category": "comment",
        "content": [{"format": "plainText", "text": "mycontent"}],
        "instrument": "id00",
    }
    assert message == expected
    assert messages.empty()


def test_elogbook_data(elogbook_client):
    client, messages = elogbook_client
    client.send_binary_data(
        b"123", mimetype="application/octet-stream", beamline="id00", proposal="hg123"
    )
    message = messages.get(timeout=10)
    assert message.pop("apikey")
    assert message.pop("creationDate")
    assert message.pop("machine")
    assert message.pop("software").startswith("pyicat-plus")
    data = message.pop("base64")
    data = data.replace("data:application/octet-stream;base64,", "")
    assert base64.b64decode(data.encode()) == b"123"
    expected = {"investigation": "hg123", "instrument": "id00"}
    assert message == expected
    assert messages.empty()


def test_elogbook_data_beamline_only(elogbook_client):
    client, messages = elogbook_client
    client.send_binary_data(
        b"123", mimetype="application/octet-stream", beamline="id00"
    )
    message = messages.get(timeout=10)
    assert message.pop("apikey")
    assert message.pop("creationDate")
    assert message.pop("machine")
    assert message.pop("software").startswith("pyicat-plus")
    data = message.pop("base64")
    data = data.replace("data:application/octet-stream;base64,", "")
    assert base64.b64decode(data.encode()) == b"123"
    expected = {"instrument": "id00"}
    assert message == expected
    assert messages.empty()
