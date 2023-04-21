import uuid
import json
import modules.connection_utils.connection_utils
from modules.connection_utils.connection_utils import send_request
from modules.constants.routings import R_AUTH

with open("currentdata.json", "r") as f:
    data = json.load(f)

name = data["nickname"]
token = data["token"]


def test_init_auth():
    response = send_request(R_AUTH, nickname=name, password="qwerty")
    assert response["success"]
    assert response["accessToken"] == token
    assert "error" not in response.keys() or response['error'] is None


def test_repeated_auth():
    response_first = send_request(R_AUTH, nickname=name, password="qwerty")
    response_second = send_request(R_AUTH, nickname=name, password="qwerty")
    response_third = send_request(R_AUTH, nickname=name, password="qwerty")
    assert response_first["accessToken"] == response_second["accessToken"] == response_third["accessToken"] == token


def test_bad_data_auth():
    response = send_request(R_AUTH, nickname=str(uuid.uuid4()) + str(uuid.uuid4()) + str(uuid.uuid4()),
                            password="qwerty")
    assert not response["success"]
    assert response["exception"]["message"] is not None
