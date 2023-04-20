import random
from itertools import permutations

import requests
import pytest
from main import *
from test_main import *


cards = []
# TODO check token
def test_creating_room():
    res = send_request('/set/room/create', accessToken=TOKEN)
    check_response(res, success=True, exception=None, gameId=None)

    res = send_request('/set/room/create', accessToken=TOKEN)
    check_response(res, success=False, exception=None)

def test_joining_room():
    # TODO Регистрация нового юзера и присоединение к комнате
    pass

def test_leaving_room():
    # TODO Выход с обоих юзеров
    pass


def test_field():
    res = send_request('set/field', accessToken=TOKEN)
    check_response(res, success=False, exception=None)

    send_request('/set/room/create', accessToken=TOKEN)
    res = send_request('/set/field', accessToken=TOKEN)
    check_response(res, success=True, exception=None, cards=None, score=None)
    global cards
    cards = res[cards]
    assert cards.length == 12
    send_request('/set/room/leave', accessToken=TOKEN)


def test_add():
    res = send_request('set/add', accessToken=TOKEN)
    check_response(res, success=False, exception=None)

    send_request('/set/room/create', accessToken=TOKEN)
    cards = send_request('/set/field', accessToken=TOKEN)
    cur_len = cards.length
    while cur_len <= 21:
        cur_len += 3
        res = send_request('/set/add', accessToken=TOKEN)
        check_response(res, success=True, exception=None, cards=None)
        assert cur_len == res[cards].length
    res = send_request('set/add', accessToken=TOKEN)
    check_response(res, success=False, exception=None)
    send_request('/set/room/leave', accessToken=TOKEN)


def test_pick():
    chosen_cards = select_three_cards()
    res = send_request('/set/pick', accessToken=TOKEN, cards=chosen_cards)
    check_response(res, success=True, exception=None, isSet=None, status='ongoing')
    new_len = res['cards'].length
    assert res['isSet']

    assert new_len >= 12 and new_len <= 21

    res = send_request('/set/pick', accessToken=TOKEN, cards=chosen_cards)
    check_response(res, success=False, exception=None, status='ongoing')

    chosen_cards = select_three_cards(set=False)
    res = send_request(accessToken=TOKEN, cards=chosen_cards, status='ongoing')
    assert not res['isSet']
# TODO Реализовать игру
# TODO Проверка на exception (ну тоже с комнатой)
# TODO Добавить поле на проверку статуса игры anywhere


def test_imitate_game():
    out_cards = 0
    global cards
    chosen_cards = []
    res = {}
    flag = False
    while out_cards < 81 and flag:
        # TODO Подумать с кол-вом карт. Чтобы не зациклился.
        chosen_cards = select_three_cards(set=False)
        res = send_request('/set/pick', accessToken=TOKEN, cards=chosen_cards)
        check_response(res, success=True, exception=None, isSet=None)
        assert not res['isSet']

        chosen_cards = select_three_cards()
        res = send_request('/set/pick', accessToken=TOKEN, cards=chosen_cards)
        check_response(res, success=True, exception=None, isSet=None)
        flag = res['isSet']
        assert flag
        out_cards += 3
        # TODO update cards
    assert res['status'] == 'ended'


def select_three_cards(set=True):
    '''
    Selects three cards and returns a list of it \n
    :param set: choose three set cards
    :return: list of three cards
    '''
    global cards
    for chosen_cards in permutations(cards, 3):
        set_cards = [chosen_cards[0], chosen_cards[1], chosen_cards[1]]
        if is_set(set_cards) and set or not (is_set(cards) or set):
            return set_cards
    return []


def is_set(cards):
    for prop in PROPERTIES:
        if (cards[0][prop] == cards[1][prop] and cards[1][prop] == cards[2][prop]) or \
            (cards[0][prop] != cards[1][prop] and cards[1][prop] != cards[2][prop] and
            cards[0][prop] != cards[2][prop]):
            return True
    return False

