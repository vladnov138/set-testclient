import requests
from modules.connection_utils.connection_utils import get_test_user_name
from modules.connection_utils.connection_utils import get_full_ip
from modules.connection_utils.connection_utils import send_request
from modules.constants.routings import R_REGISTER
from modules.connection_utils.connection_utils import set_token
from modules.connection_utils.connection_utils import get_token

test_name = get_test_user_name()
password = "qwerty"
full_ip = get_full_ip()
token = None


def test_initial_register():
    response = send_request(R_REGISTER, nickname=test_name, password=password)
    assert response["success"]
    assert response["accessToken"] is not None
    set_token(response["accessToken"])
    assert response["nickname"] == test_name


def test_repeated_register():
    response = send_request(R_REGISTER, nickname=test_name, password=password)
    assert not response["success"]
    assert response["exception"] is not None
    assert response["exception"]["message"] is not None
