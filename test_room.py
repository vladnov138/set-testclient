from itertools import permutations

from main import PROPERTIES
from test_main import *


# TODO check token
# TODO Проверка вида карты
def test_creating_room():
    send_request('/set/room/leave', accessToken=token)
    res = send_request('/set/room/create', accessToken=token)
    check_response(res, success=True, exception=None, gameId=None)

    res = send_request('/set/room/create', accessToken=token)
    check_response(res, success=False, exception=None)

    send_request('/set/room/leave', accessToken=token)

def test_list_room():
    pass

def test_joining_room():
    # TODO Регистрация нового юзера и присоединение к комнате
    pass

def test_leaving_room():
    # TODO Выход с обоих юзеров
    pass


def test_field():
    send_request('/set/room/leave', accessToken=token)
    res = send_request('/set/field', accessToken=token)
    check_response(res, success=False, exception=None)

    send_request('/set/room/create', accessToken=token)
    res = send_request('/set/field', accessToken=token)
    check_response(res, success=True, exception=None, fieldCards=None, scores=None, status='ongoing')
    cards = res['fieldCards']
    assert len(cards) == 12
    send_request('/set/room/leave', accessToken=token)


def test_add():
    send_request('/set/room/leave', accessToken=token)
    res = send_request('/set/add', accessToken=token)
    check_response(res, success=False, exception=None)

    send_request('/set/room/create', accessToken=token)
    cards = send_request('/set/field', accessToken=token)['fieldCards']
    cur_len = len(cards)
    while cur_len < 21:
        res = send_request('/set/add', accessToken=token)
        check_response(res, success=True, exception=None)
        cur_cards = send_request('/set/field', accessToken=token)['fieldCards']
        cur_len += 3
        assert cur_len == len(cur_cards)
    res = send_request('/set/add', accessToken=token)
    check_response(res, success=False, exception=None)
    send_request('/set/room/leave', accessToken=token)


def test_pick():
    # TODO score
    send_request('/set/room/leave', accessToken=token)
    res = send_request('/set/pick', accessToken=token, cards=[1, 2, 3])
    check_response(res, success=False, exception=None)

    send_request('/set/room/create', accessToken=token)
    res = send_request('/set/field', accessToken=token)
    cards = res['fieldCards']
    old_scores = res['score']
    chosen_cards = select_three_cards(cards)
    res = send_request('/set/pick', accessToken=token, cards=chosen_cards)
    print(res)
    check_response(res, success=True, exception=None, isSet=True)
    new_res = send_request('/set/field', accessToken=token)
    new_scores = new_res['score']
    new_len = len(new_res['fieldCards'])

    assert new_len >= 12 and new_len <= 21 # TODO ?
    assert new_scores > old_scores

    res = send_request('/set/pick', accessToken=token, cards=chosen_cards)
    check_response(res, success=False, exception=None)

    cards = send_request('/set/field', accessToken=token)['fieldCards']
    old_scores = new_scores
    chosen_cards = select_three_cards(cards, set=False)
    res = send_request('/set/pick', accessToken=token, cards=chosen_cards)
    check_response(res, success=True, exception=None, isSet=False)
    assert old_scores <= res['scores']
    send_request('/set/room/leave', accessToken=token)


def test_imitate_game():
    send_request('/set/room/leave', accessToken=token)
    send_request('/set/room/create', accessToken=token)
    out_cards = 0
    res = {}
    status = 'ongoing'
    cards = send_request('/set/field', accessToken=token)['cards']
    while out_cards < 81 and status == 'ongoing':
        chosen_cards = select_three_cards(cards, set=False)
        res = send_request('/set/pick', accessToken=token, cards=chosen_cards)
        check_response(res, success=True, exception=None, isSet=False, status=None)

        chosen_cards = select_three_cards(cards)
        while len(chosen_cards) == 0:
            cards = send_request('/set/add', accessToken=token)
            chosen_cards = select_three_cards(cards)
        res = send_request('/set/pick', accessToken=token, cards=chosen_cards)
        check_response(res, success=True, exception=None, isSet=True, status=None)
        status = res['status']
        cards = send_request('set/field', accessToken=token)['cards']
        out_cards += 3
    assert res['status'] == 'ended' and out_cards > 60


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

