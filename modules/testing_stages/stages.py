import subprocess
import uuid
from datetime import datetime
from pathlib import Path

import modules.connection_utils.connection_utils
from modules.connection_utils.connection_utils import is_localhost
from modules.connection_utils.connection_utils import MODE

from modules.connection_utils.connection_utils import get_random_localhost_meme

from modules.connection_utils.connection_utils import set_full_ip
from modules.connection_utils.connection_utils import set_server_ip
from modules.connection_utils.connection_utils import get_full_ip
import json

styles = ["""
	<style>
		body {
			background-color: #000;
		}

		h2 {
			font-size: 4em;
			text-align: center;
			font-family: sans-serif;
			text-transform: uppercase;
			letter-spacing: 0.1em;
			padding: 0.5em;
			margin: 1em 0;
			box-shadow: 0 0 20px #fff;
		}

		h2.success {
			color: #0f0;
		}

		h2.failure {
			color: #f00;
		}
	</style>
	"""]


def process_ip_stage(ip: str, port: str, mode: int):
    """Processes ip-checking stage of the testing"""
    if is_localhost(ip) and mode:
        return "".join([f'<img src="{get_random_localhost_meme()}"><br>', "<h2>Мы локалхост не топим!</h2>"]), False
    set_full_ip(ip, port)
    result_ip = f"{ip}:{port}"
    set_server_ip(result_ip)
    file_name = str(uuid.uuid4()) + ".log"
    init_tests_cmd = f"pytest tests/test_ip.py > {file_name}"
    subprocess.call(init_tests_cmd, shell=True)
    file_data = []

    has_ip_fails = False
    with open(file_name, "r") as f:
        lines = [line + "<br>" for line in f]
        for i in lines:
            if "FAILURES" in i or "FAILED" in i or "ERRORS" in i:
                has_ip_fails = True
                break
    Path(file_name).unlink()
    if has_ip_fails:
        link = modules.connection_utils.connection_utils.IP_TESTS_FAILED
        file_data += ['<h2 class="failure">IP TEST STATUS: FAILED! </h2>',
                      f'<br><img src="{link}"><br>', ]
    else:
        file_data.append('<h2 class="success">IP TEST STATUS: SUCCESS!</h2>')
    return file_data, not has_ip_fails


def process_register_stage():
    """Tests for the registration function"""
    result = []
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
        for i in lines:
            if "FAILURES" in i:
                has_register_fails = True
                result.append('<h2 class="failure">REGISTRATION TEST STATUS: FAILED!</h2>')
                break
    if not has_register_fails:
        result.append('<h2 class="success">REGISTRATION TEST STATUS: SUCCESS!</h2>')
    # Path(file_name).unlink()
    return result, not has_register_fails


def process_auth_stage():
    result = []
    file_name = str(uuid.uuid4()) + ".log"
    init_tests_cmd = f"pytest tests/test_auth.py > {file_name}"
    subprocess.call(init_tests_cmd, shell=True)
    has_register_fails = False
    with open(file_name, "r") as f:
        lines = [line + "<br>" for line in f]
        for i in lines:
            if "FAILURES" in i:
                has_register_fails = True
                result.append('<h2 class="failure">AUTH TESTS STATUS: FAILED!<h2>')
                break
    if not has_register_fails:
        result.append('<h2 class="success">AUTH TESTS STATUS: SUCCESS!</h2>')
    # Path(file_name).unlink()
    return result, not has_register_fails


def process_game_stage():
    result = []
    file_name = str(uuid.uuid4()) + ".log"
    init_tests_cmd = f"pytest tests/test_game.py > {file_name}"
    subprocess.call(init_tests_cmd, shell=True)
    has_game_fails = False
    with open(file_name, "r") as f:
        lines = [line + "<br>" for line in f]
        for i in lines:
            if "FAILURES" in i:
                has_game_fails = True
                result.append('<h2 class="failure">GAME TESTS STATUS: FAILED!<h2>')
                break
    if not has_game_fails:
        result.append('<h2 class="success">GAME TESTS STATUS: SUCCESS!</h2>')
        result.append('<h2 class="success">ALL TESTS WERE SUCCESSFULLY PASSED! CONGRATULATIONS!</h2>')
    # Path(file_name).unlink()
    return result, not has_game_fails


def process_all(ip: str, port: str, server_mode: int, room_mode: int):
    init_result, continue_status = process_ip_stage(ip, port, server_mode)
    if continue_status:
        register_result, continue_status = process_register_stage()
        if continue_status:
            register_result.append('<h2 class="success">AUTH TESTS STATUS: SUCCESS!</h2>')
            game_result, continue_status = process_game_stage()
            return "".join(styles + register_result + game_result)
        return "".join(styles + init_result + register_result)
    return "".join(styles + init_result)
