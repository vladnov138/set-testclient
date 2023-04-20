import requests
import pytest
from main import URL, TOKEN, PROPERTIES, cards

body = {'accessToken': TOKEN}


def test_field():
    res = requests.post(URL + "/set/field", data=body).json()


def test_add():
    res = requests.post(URL + "set/add", data=body).json()


def test_pick():
    res = requests.post(URL + "set/pick", data=body).json()


def find_set():
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            for k in range(j + 1, len(cards)):
                set_cards = [cards[i], cards[j], cards[k]]
                if is_set(set_cards):
                   return set_cards
    return []


def is_set(cards):
    for prop in PROPERTIES:
        if (cards[0][prop] == cards[1][prop] and cards[1][prop] == cards[2][prop]) or \
            (cards[0][prop] != cards[1][prop] and cards[1][prop] != cards[2][prop] and
            cards[0][prop] != cards[2][prop]):
            return True
    return False