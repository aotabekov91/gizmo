import pytest
from qapp.core.modes import Mode

@pytest.fixture
def mode(): return Mode()

def test_import(mode): assert mode

