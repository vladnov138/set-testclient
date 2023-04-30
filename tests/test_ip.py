# Basic init checks for the input data
import re
import modules.connection_utils.connection_utils

CURRENT_IP = modules.connection_utils.connection_utils.get_server_ip()


def test_ip_len():
    """Checks IP length"""
    result = CURRENT_IP is not None and len(CURRENT_IP) != 0 and 7 <= len(CURRENT_IP) <= 15
    assert result


def test_ip_pattern():
    """Checks if the input ip corresponds to the pattern"""
    pattern = re.compile(
        r'^(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)\.(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    assert pattern.match(CURRENT_IP)


def test_ip_online():
    """Checks if IP is offline"""
    assert modules.connection_utils.connection_utils.is_ip_online(CURRENT_IP)
