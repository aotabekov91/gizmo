import pytest
from qapp.plug import PlugObj

@pytest.fixture
def plug_obj():
    return PlugObj()

def test_initial(plug_obj):
    assert plug_obj

