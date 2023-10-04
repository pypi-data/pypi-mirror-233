from datetime import datetime
import xml.etree.ElementTree as etree
from .serialize import serialize_metadata

ICAT_NAMESPACE_URL = "http://www.esrf.fr/icat"

etree.register_namespace("tns", ICAT_NAMESPACE_URL)


def root_node(name: str, **kw):
    return etree.Element(f"{{{ICAT_NAMESPACE_URL}}}{name}", **kw)


def child_node(parent, name: str, **kw):
    return etree.SubElement(parent, f"{{{ICAT_NAMESPACE_URL}}}{name}", **kw)


def encode_node_data(data) -> str:
    text = serialize_metadata(data)
    if not isinstance(text, str):
        raise ValueError(data)
    return text


def data_node(parent, name: str, data, **kw):
    node = child_node(parent, name, **kw)
    node.text = encode_node_data(data)


def parameter_node(parent, name: str, value, **kw):
    node = child_node(parent, "parameter", **kw)
    data_node(node, "name", name)
    data_node(node, "value", value)


def dataset_as_xml(
    beamline: str, proposal: str, dataset: str, path: str, metadata: dict = None
):
    assert beamline, "ICAT requires the beamline name"
    assert proposal, "ICAT requires the proposal name"
    assert dataset, "ICAT requires the dataset name"
    assert path, "ICAT requires the dataset path"
    if metadata is None:
        metadata = dict()

    # Required metadata
    assert "Sample_name" in metadata, "ICAT metadata field 'Sample_name' is missing"

    # Metadata with defaults
    if "startDate" not in metadata:
        metadata["startDate"] = datetime.now()
    if "endDate" not in metadata:
        metadata["endDate"] = datetime.now()

    root = root_node("dataset", attrib={"complete": "true"})
    data_node(root, "investigation", proposal)
    data_node(root, "instrument", beamline)
    data_node(root, "name", dataset)
    data_node(root, "location", path)

    metadata = serialize_metadata(metadata)
    for name, value in metadata.items():
        parameter_node(root, name, value)
        # Metadata included in the XML tree
        if name == "Sample_name":
            sample = child_node(root, "sample")
            data_node(sample, "name", value)
        elif name == "startDate":
            data_node(root, "startDate", value)
        elif name == "endDate":
            data_node(root, "endDate", value)

    return root


def investigation_as_xml(beamline: str, proposal: str, start_datetime=None):
    root = root_node("investigation")
    data_node(root, "experiment", proposal)
    data_node(root, "instrument", beamline)
    if start_datetime is None:
        start_datetime = datetime.now()
    data_node(root, "startDate", start_datetime)
    return root
