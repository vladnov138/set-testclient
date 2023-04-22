from itertools import permutations
import requests

from main import PROPERTIES

url = ""
token1 = ""
token2 = ""
gameId = 0

def test_register():
    res = register("vanka", '242424')
    print(res)
    check_response(res, success=True, exception=None, accessToken=None, nickname=None)
    global token1
    token1 = res["accessToken"]

    res = register("Ivan_Sergeevich", 'PipecGU')
    check_response(res, success=True, exception=None, accessToken=None, nickname=None)
    global token2
    token2 = res["accessToken"]


def get_gamelist(token=token1):
    return send_request('/set/room/list', accessToken=token)


def send_request(route: str, **kwargs) -> dict:
    '''
    Sends request to the route
    :param route: request route
    :param kwargs: request body
    :return: request result
    '''
    return requests.post(url+route, json=kwargs, headers={"Content-type": "application/json"}).json()


def check_response(resp: dict, **kwargs) -> None:
    '''
    Checks fields in the response
    :param resp: request response
    :param kwargs: necessary fields
    '''
    for key in kwargs:
        assert key in resp
        if kwargs[key] is not None:
            assert resp[key] == kwargs[key]


def register(nickname: str, password: str) -> dict:
    '''
    Registers or authenticates user
    :param nickname: user's nickname
    :param password: user's password
    :return: request result
    '''
    return send_request("/user/register", nickname=nickname, password=password)


def add_cards(token=token1) -> dict:
    '''
    Adds 3 cards to the field
    :return: request result
    '''
    return send_request('/set/add', accessToken=token)


def get_field(token=token1) -> dict:
    '''
    Gets field
    :return: request result
    '''
    return send_request('/set/field', accessToken=token)


def pick(chosen_cards, token=token1) -> dict:
    '''
    Picks chosen cards and checks it for set
    :param chosen_cards: list of three chosen cards
    :return: request result
    '''
    return send_request('/set/pick', accessToken=token, cards=chosen_cards)


def create_room(token=token1) -> dict:
    '''
    Creating a room
    :return: request result
    '''
    return send_request('/set/room/create', accessToken=token)


def leave(token=token1) -> dict:
    '''
    Leaving the room
    :return: request result
    '''
    return send_request('/set/room/leave', accessToken=token)


def select_three_cards(cards: list, set=True) -> list:
    '''
    Selects three cards and returns a list of it \n
    :param cards: list of cards on the field
    :param set: choose set cards
    :return: list of three cards or empty list
    '''
    for chosen_cards in permutations(cards, 3):
        set_cards = [chosen_cards[0], chosen_cards[1], chosen_cards[2]]
        if is_set(set_cards) and set or not (is_set(set_cards) or set):
            return [chosen_cards[0]['id'], chosen_cards[1]['id'], chosen_cards[2]['id']]
    return []


def is_set(cards: list) -> bool:
    '''
    Checks chosen cards if it's set
    :param cards: list of three cards
    :return: true if it's set
    '''
    for prop in PROPERTIES:
        if not ((cards[0][prop] == cards[1][prop] and cards[1][prop] == cards[2][prop]) or
            (cards[0][prop] != cards[1][prop] and cards[1][prop] != cards[2][prop] and
             cards[0][prop] != cards[2][prop])):
            return False
    return True
