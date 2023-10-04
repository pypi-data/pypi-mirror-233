from ..modules.service.auth import Authenticate
from pytest import raises

def test_auth_raises_valueerror_if_no_configfile_present():
    with raises(ValueError, match=r"Cannot find config file,.*"):
        Authenticate()