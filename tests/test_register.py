import requests

import modules.connection_utils.connection_utils
from modules.connection_utils.connection_utils import get_full_ip
from modules.connection_utils.connection_utils import send_request
from modules.constants.routings import R_REGISTER
from modules.connection_utils.connection_utils import set_token
import json


USER1_FILE = "userdata_1.json"
USER2_FILE = "userdata_2.json"

with open(USER1_FILE, "r") as f:
    data = json.load(f)


test_name = data["nickname"]
password = "qwerty"

full_ip = get_full_ip()
token = None


def test_initial_register():
    response = send_request(R_REGISTER, nickname=test_name, password=password)
    assert response["success"]
    assert response["accessToken"] is not None
    with open('userdata_1.json', "r+") as f:
        dictionary = json.load(f)
        dictionary["token"] = response["accessToken"]
        f.seek(0)
        json.dump(dictionary, f)
    assert response["nickname"] == test_name


def test_wrong_password():
    response = send_request(R_REGISTER, nickname=test_name, password="123")
    assert not response["success"]


"""
Удалён, тк кто-то решил, что вешать и авторизацию и регистрацию на один роутинг будет ахуенной идеей
def test_repeated_register():
    response = send_request(R_REGISTER, nickname=test_name, password=password)
    assert not response["success"]
    assert response["exception"] is not None
    assert response["exception"]["message"] is not None
"""

def test_register_extra_user():
    with open(USER2_FILE, "r") as f:
        user_data = json.load(f)
        c_name = user_data["nickname"]
        c_password = "qwerty"
        response = send_request(R_REGISTER, nickname=c_name, password=c_password)
    assert response["success"]
    assert response["accessToken"] is not None
    with open(USER2_FILE, "r+") as f:
        dictionary = json.load(f)
        dictionary["token"] = response["accessToken"]
        print(dictionary)
        f.seek(0)
        json.dump(dictionary, f)
