import subprocess
import uuid
from datetime import datetime
from pathlib import Path

import modules.connection_utils.connection_utils
from modules.connection_utils.connection_utils import set_server_ip
from modules.connection_utils.connection_utils import is_localhost
from modules.connection_utils.connection_utils import MODE

from modules.connection_utils.connection_utils import get_random_localhost_meme

from modules.connection_utils.connection_utils import set_full_ip
from modules.connection_utils.connection_utils import get_full_ip
import json


def process_ip_stage(ip: str, port: str, mode: int):
    """Processes ip-checking stage of the testing"""
    if is_localhost(ip) and mode:
        return "".join([f'<img src="{get_random_localhost_meme()}"><br>', "<h2>Мы локалхост не топим!</h2>"]), False
    result_ip = f"{ip}:{port}"
    set_full_ip(ip, port)
    set_server_ip(result_ip)
    file_name = str(uuid.uuid4()) + ".log"
    init_tests_cmd = f"pytest tests/test_ip.py > {file_name}"
    subprocess.call(init_tests_cmd, shell=True)
    file_data = [
        "=" * 100 + "<br><br>",
        "<h3>IP Init Tests</h3>",
        f"SERVER IP: {ip}<br>",
        f"SERVER PORT: {port}<br>",
        f"TESTS LOGS: {file_name} <br>",
        f"TEST STARTED AT: {datetime.now().strftime('%H:%M:%S')}<br>",
        f"CURRENT STAGE: INPUT IP TEST <br><br>",
        "=" * 100 + "<br><br>",
    ]

    has_ip_fails = False
    with open(file_name, "r") as f:
        lines = [line + "<br>" for line in f]
        file_data += lines
        for i in lines:
            if "FAILURES" in i:
                has_ip_fails = True
                break
    Path(file_name).unlink()
    if has_ip_fails:
        link = modules.connection_utils.connection_utils.IP_TESTS_FAILED
        file_data += [f'<br><img src="{link}"><br>',
                      "<h2>У вас ошибка связанная с IP адресом, дальнейшее тестирование не будет проведено!</h2>"]
    else:
        file_data.append("<h2>Ip stage status: SUCCESS!</h2>")
    return file_data, not has_ip_fails


def process_register_stage():
    """Tests for the registration function"""
    result = ["<br><br><br>" + "=" * 100,
              "<br><br><h3> Registration Tests </h3><br><br>",
              "=" * 100]
    file_name = str(uuid.uuid4()) + ".log"

    test_name = "test_user_" + str(uuid.uuid4())
    data = {"nickname": test_name, "password": "qwerty"}
    data_extra = {"nickname": test_name + "_buddy", "password": "qwerty"}
    with open("userdata_1.json", "w") as f:
        json.dump(data, f)

    with open("userdata_2.json", "w") as f:
        json.dump(data_extra, f)
    init_tests_cmd = f"pytest tests/test_register.py > {file_name}"
    subprocess.call(init_tests_cmd, shell=True)
    has_register_fails = False
    with open(file_name, "r") as f:
        lines = [line + "<br>" for line in f]
        result += lines
        for i in lines:
            if "FAILURES" in i:
                has_register_fails = True
                result.append('<h2>У вас ошибки в блоке "Регистрация"! Дальнейшее тестирование проведено не будет! ')
                break
    if not has_register_fails:
        result.append("<h3>Register Stage Status: SUCCESS!</h3>")
    Path(file_name).unlink()
    return result, not has_register_fails


def process_auth_stage():
    result = ["<br><br><br>" + "=" * 100,
              "<br><br><h3> Authorization Tests </h3><br><br>",
              "=" * 100]
    file_name = str(uuid.uuid4()) + ".log"
    init_tests_cmd = f"pytest tests/test_auth.py > {file_name}"
    subprocess.call(init_tests_cmd, shell=True)
    has_register_fails = False
    with open(file_name, "r") as f:
        lines = [line + "<br>" for line in f]
        result += lines
        for i in lines:
            if "FAILURES" in i:
                has_register_fails = True
                result.append('<h2>У вас ошибки в блоке "Авторизация"! Дальнейшее тестирование проведено не будет! ')
                break
    if not has_register_fails:
        result.append("<h3>Authorization Stage Status: SUCCESS!</h3>")
    Path(file_name).unlink()
    return result, not has_register_fails


def process_all(ip: str, port: str, server_mode: int, room_mode: int):
    init_result, continue_status = process_ip_stage(ip, port, server_mode)
    if continue_status:
        register_result, continue_status = process_register_stage()
        if continue_status:
            auth_result, continue_status = process_auth_stage()
            return "".join(init_result + register_result + auth_result)
        return "".join(init_result + register_result)
    return init_result
