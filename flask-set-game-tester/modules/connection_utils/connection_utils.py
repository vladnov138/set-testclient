import uuid

import requests
import random

SERVER_IP = "127.0.0.1"
SERVER_IP_FULL = "http://127.0.0.1:4567"

MODE_GLOBAL = 1
MODE_LOCAL = 0
MODE = MODE_LOCAL

ROOM_SINGLE = 0
ROOM_MULTIPLE = 1
ROOM_MODE = ROOM_SINGLE

TOKEN = "qwerty"

LOCALHOST_MEMES = [
    "https://i.ibb.co/J2nTYF0/1.jpg",
    "https://i.ibb.co/hZKGY3f/2.jpg",
    "https://i.ibb.co/JvSXyZ3/3.jpg",
    "https://i.ibb.co/pnRgsBL/4.jpg",
    "https://i.ibb.co/64dG4wZ/5.jpg",
    "https://i.ibb.co/d4C48TX/6.jpg"

]

IP_TESTS_FAILED = "https://www.meme-arsenal.com/memes/526c27ae2deb49e11536fc09999d2042.jpg"


def get_server_ip():
    global SERVER_IP
    return SERVER_IP


def set_server_ip(ip: str):
    global SERVER_IP
    SERVER_IP = ip


def set_full_ip(ip: str, port: str):
    global SERVER_IP_FULL
    SERVER_IP_FULL = "http://" + ip + ":" + port


def get_full_ip():
    return SERVER_IP_FULL


def is_ip_online(ip_address="127.0.0.1", port=80):
    """Checks if IP is online"""
    sock: socket.socket = None
    if MODE:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((ip_address, port))
            return not result
        except Exception as e:
            return False
        finally:
            if sock is not None:
                sock.close()
    return True


def is_localhost(ip: str):
    """Checks if the input ip belongs to localhost"""
    localhosts = ["127.0.0.1",
                  "127.0.0.0",
                  "0.0.0.0",
                  "localhost"]
    return ip in localhosts


def get_random_localhost_meme():
    """Returns link to the random localhost meme"""
    return random.choice(LOCALHOST_MEMES)


def send_request(route, **kwargs):
    return requests.post(get_full_ip() + route, json=kwargs, headers={"Content-type": "application/json"}).json()


def set_server_mode(mode: int):
    global MODE
    MODE = mode


def set_room_mode(mode: int):
    global ROOM_MODE
    ROOM_MODE = mode


def set_token(token: str):
    global TOKEN
    TOKEN = token


def get_token():
    return TOKEN
