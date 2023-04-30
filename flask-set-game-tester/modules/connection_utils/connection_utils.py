import uuid
import requests
import random
from itertools import permutations
SERVER_IP = "127.0.0.1"
SERVER_IP_FULL = "http://127.0.0.1:4567"
PROPERTIES = ['color', 'count', 'shape', 'fill']
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
    print(get_full_ip() + route)
    return requests.post("http://84.252.142.21:8080/api" + route, json=kwargs, headers={"Content-type": "application/json"}).json()


def set_server_mode(mode: int):
    global MODE
    MODE = mode


def set_room_mode(mode: int):
    global ROOM_MODE
    ROOM_MODE = mode


def set_token(token: str):
    global TOKEN
    TOKEN = token


def get_gamelist(token: str):
    return send_request('/set/room/list', accessToken=token)


def add_cards(token: str) -> dict:
    """
    Adds 3 cards to the field
    :return: request result
    """
    return send_request('/set/add', accessToken=token)


def get_field(token: str) -> dict:
    """
    Gets field
    :return: request result
    """
    return send_request('/set/field', accessToken=token)


def pick(chosen_cards, token: str) -> dict:
    """
    Picks chosen cards and checks it for set
    :param chosen_cards: list of three chosen cards
    :return: request result
    """
    return send_request('/set/pick', accessToken=token, cards=chosen_cards)


def create_room(token: str) -> dict:
    """
    Creating a room
    :return: request result
    """
    return send_request('/set/room/create', accessToken=token)


def leave(token: str) -> dict:
    """
    Leaving the room
    :return: request result
    """
    return send_request('/set/room/leave', accessToken=token)


def select_three_cards(cards: list, set=True) -> list:
    """
    Selects three cards and returns a list of it \n
    :param cards: list of cards on the field
    :param set: choose set cards
    :return: list of three cards or empty list
    """
    for chosen_cards in permutations(cards, 3):
        set_cards = [chosen_cards[0], chosen_cards[1], chosen_cards[2]]
        if is_set(set_cards) and set or not (is_set(set_cards) or set):
            return [chosen_cards[0]['id'], chosen_cards[1]['id'], chosen_cards[2]['id']]
    return []


def is_set(cards: list) -> bool:
    """
    Checks chosen cards if it's set
    :param cards: list of three cards
    :return: true if it's set
    """
    for prop in PROPERTIES:
        if not ((cards[0][prop] == cards[1][prop] and cards[1][prop] == cards[2][prop]) or
                (cards[0][prop] != cards[1][prop] and cards[1][prop] != cards[2][prop] and
                 cards[0][prop] != cards[2][prop])):
            return False
    return True


def check_response(resp: dict, **kwargs) -> None:
    """
    Checks fields in the response
    :param resp: request response
    :param kwargs: necessary fields
    """
    for key in kwargs:
        assert key in resp
        if kwargs[key] is not None:
            assert resp[key] == kwargs[key]
