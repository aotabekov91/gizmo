import pytest
from qapp.plug import Plug

@pytest.fixture
def plug_obj():
    return Plug()

def test_initial(plug_obj):
    assert plug_obj

