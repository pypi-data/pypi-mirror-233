import pytest
from .fixtures.icat import *  # noqa F401

from ..metadata.definitions import load_icat_fields


@pytest.fixture
def icat_fields():
    return load_icat_fields()
