import random

#TODO create constants module

SERVER_IP = "127.0.0.1"

MODE_GLOBAL = 1
MODE_LOCAL = 0
MODE = MODE_GLOBAL

#TODO: add more memes
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
    """Returns actual test server IP"""
    global SERVER_IP
    return SERVER_IP


def set_server_ip(ip: str):
    """Sets IP of the test server"""
    global SERVER_IP
    SERVER_IP = ip


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
