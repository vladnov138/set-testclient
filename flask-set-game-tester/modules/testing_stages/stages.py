import subprocess
import uuid
from datetime import datetime
from pathlib import Path

import modules.connection_utils.connection_utils
from modules.connection_utils.connection_utils import set_server_ip
from modules.connection_utils.connection_utils import is_localhost
from modules.connection_utils.connection_utils import MODE
from modules.connection_utils.connection_utils import get_random_localhost_meme


def process_ip_stage(ip: str, port: str):
    """Processes ip-checking stage of the testing"""
    if is_localhost(ip) and MODE:
        return "".join([f'<img src="{get_random_localhost_meme()}"><br>', "<h2>Мы локалхост не топим!</h2>"]), False
    result_ip = f"{ip}:{port}"
    set_server_ip(result_ip)
    file_name = str(uuid.uuid4()) + ".log"
    init_tests_cmd = f"pytest tests/test_ip.py > {file_name}"
    subprocess.call(init_tests_cmd, shell=True)
    file_data = [
        "=" * 100 + "<br><br>",
        f"SERVER IP: {ip}<br>",
        f"SERVER PORT: {port}<br>",
        f"TESTS LOGS: {file_name} <br>",
        f"TEST STARTED AT: {datetime.now().strftime('%H:%M:%S')}<br>",
        f"CURRENT STAGE: INPUT IP TEST <br><br>"
        "=" * 100 + "<br><br>",

    ]
    # Checks if this stage was failed one or more times 
    has_ip_fails = False
    with open(file_name, "r") as f:
        lines = [line + "<br>" for line in f]
        file_data += lines
        for i in lines:
            if "FAILURES" in i:
                has_ip_fails = True
                break
    Path(file_name).unlink()
    continue_status = True
    # If the test case(s) was/were failed
    if has_ip_fails:
        link = modules.connection_utils.connection_utils.IP_TESTS_FAILED
        file_data += [f'<br><img src="{link}"><br>',
                      "<h2>У вас ошибка связанная с IP адресом, дальнейшее тестирование не будет проведено!</h2>"]
        continue_status = False
    return "".join(file_data), continue_status
