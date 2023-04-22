from test_main import *
from functions import *


# TODO check token
def test_creating_room():
    leave()
    res = create_room()
    check_response(res, success=True, exception=None, gameId=None)

    res = create_room()
    check_response(res, success=False, exception=None)
    leave()


def test_list_room():
    leave()
    res = get_gamelist()
    check_response(res, success=True, exception=None, games=None)
    assert len(res['games']) >= 0


def test_cards():
    leave()
    create_room()
    res = get_field()
    check_response(res, success=True, exception=None, fieldCards=None)
    card = res['fieldCards'][11]
    check_response(card, count=None, color=None, fill=None, shape=None)


def test_room():
    leave()
    leave(token=token2)

    res = get_gamelist(token=token2)
    check_response(res, success=True, exception=None, games=None)
    count_games = len(res['games'])

    game_id = create_room()['gameId']

    res = get_gamelist(token=token2)
    check_response(res, success=True, exception=None, games=None)
    new_count_games = len(res['games'])

    assert new_count_games > count_games
    count_games = new_count_games

    res = send_request('/set/room/enter', accessToken=token2, gameId=game_id)
    print(res)
    check_response(res, success=True, exception=None, gameId=None)

    res = leave(token=token2)
    check_response(res, success=True, exception=None)
    res = leave(token=token2)
    check_response(res, success=False, exception=None)
    res = leave()
    check_response(res, success=True, exception=None)

    res = get_gamelist(token=token2)
    check_response(res, success=True, exception=None, games=None)
    new_count_games = len(res['games'])

    assert new_count_games < count_games


def test_field():
    leave()
    res = get_field()
    check_response(res, success=False, exception=None)

    create_room()
    res = get_field()
    print(res)
    check_response(res, success=True, exception=None, fieldCards=None, status='ongoing')
    cards = res['fieldCards']
    assert len(cards) == 12
    leave()


def test_add():
    leave()
    res = add_cards()
    check_response(res, success=False, exception=None)

    create_room()
    cards = get_field()['fieldCards']
    cur_len = len(cards)
    while cur_len < 21:
        res = add_cards()
        check_response(res, success=True, exception=None)
        cur_cards = get_field()['fieldCards']
        cur_len += 3
        assert cur_len == len(cur_cards)
    res = add_cards()
    check_response(res, success=False, exception=None)
    leave()


def test_pick():
    leave()
    res = pick([1, 2, 3])
    check_response(res, success=False, exception=None)

    create_room()
    res = get_field()
    cards = res['fieldCards']
    chosen_cards = select_three_cards(cards)
    while len(chosen_cards) == 0:
        add_cards()
        cards = res['fieldCards']
        chosen_cards = select_three_cards(cards)
    res = pick(chosen_cards)
    check_response(res, success=True, exception=None, isSet=True)
    new_res = get_field()
    new_len = len(new_res['fieldCards'])

    assert 12 <= new_len <= 21

    res = pick(chosen_cards)
    check_response(res, success=False, exception=None)

    cards = get_field()['fieldCards']
    chosen_cards = select_three_cards(cards, set=False)
    res = pick(chosen_cards)
    check_response(res, success=True, exception=None, isSet=False)
    leave()


def test_score():
    leave()
    create_room()
    res = send_request('/set/score', accessToken=token1)
    print(res)
    check_response(res, success=True, exception=None, users=None)
    old_score = res['users'][0]['score']
    cards = get_field()['fieldCards']
    pick(select_three_cards(cards))
    res = send_request('/set/score', accessToken=token1)
    check_response(res, success=True, exception=None, users=None)
    new_score = res['users'][0]['score']
    assert new_score > old_score


def test_imitate_game():
    leave()
    create_room()
    out_cards = 0
    status = 'ongoing'
    cards = get_field()['fieldCards']
    while out_cards < 81 and status == 'ongoing':
        chosen_cards = select_three_cards(cards, set=False)
        res = pick(chosen_cards)
        check_response(res, success=True, exception=None, isSet=False)

        chosen_cards = select_three_cards(cards)
        while len(chosen_cards) == 0:
            add_cards()
            cards = get_field()['fieldCards']
            chosen_cards = select_three_cards(cards)
        res = pick(chosen_cards)
        check_response(res, success=True, exception=None, isSet=True)

        status = get_field()['status']
        cards = get_field()['fieldCards']
        out_cards += 3
    assert status == 'ended' and out_cards > 60
    leave()

