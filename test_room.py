from test_main import *
from functions import *


# TODO check token
# TODO Проверка вида карты
def test_creating_room():
    leave()
    res = create_room()
    check_response(res, success=True, exception=None, gameId=None)

    res = create_room()
    check_response(res, success=False, exception=None)
    leave()


# TODO add new user
def test_list_room():
    leave()
    res = send_request('/set/room/list', accessToken=token)
    check_response(res, success=True, exception=None, games=None)
    assert len(res['games']) >= 0


def test_joining_room():
    leave()
    res = register("Ivan_Sergeevich", "PipecGU")
    check_response(res, success=True, exception=None, accessToken=None)
    second_token = res['accessToken']

    game_id = create_room()['gameId']
    res = send_request('/set/room/enter', accessToken=second_token, gameId=game_id)
    check_response(res, success=True, exception=None)

    res = leave(access_token=second_token)
    check_response(res, success=True, exception=None)
    res = leave(access_token=second_token)
    check_response(res, success=False, exception=None)
    res = leave()
    check_response(res, success=True, exception=None)



def test_leaving_room():
    pass


def test_field():
    leave()
    res = get_field()
    check_response(res, success=False, exception=None)

    create_room()
    res = get_field()
    check_response(res, success=True, exception=None, fieldCards=None, scores=None, status='ongoing')
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
    # TODO score
    leave()
    res = pick([1, 2, 3])
    check_response(res, success=False, exception=None)

    create_room()
    res = get_field()
    cards = res['fieldCards']
    old_scores = res['score']
    chosen_cards = select_three_cards(cards)
    res = pick(chosen_cards)
    check_response(res, success=True, exception=None, isSet=True)
    new_res = get_field()
    new_scores = new_res['score']
    new_len = len(new_res['fieldCards'])

    assert new_len >= 12 and new_len <= 21 # TODO ?
    assert new_scores > old_scores

    res = pick(chosen_cards)
    check_response(res, success=False, exception=None)

    cards = get_field()['fieldCards']
    old_scores = new_scores
    chosen_cards = select_three_cards(cards, set=False)
    res = pick(chosen_cards)
    check_response(res, success=True, exception=None, isSet=False)
    assert old_scores <= res['scores']
    leave()


def test_imitate_game():
    leave()
    create_room()
    out_cards = 0
    res = {}
    status = 'ongoing'
    cards = get_field()['cards']
    while out_cards < 81 and status == 'ongoing':
        chosen_cards = select_three_cards(cards, set=False)
        res = pick(chosen_cards)
        check_response(res, success=True, exception=None, isSet=False)

        chosen_cards = select_three_cards(cards)
        while len(chosen_cards) == 0:
            cards = add_cards()
            chosen_cards = select_three_cards(cards)
        res = pick(chosen_cards)
        check_response(res, success=True, exception=None, isSet=True)

        # status = res['status'] TODO ?
        cards = get_field()['cards']
        out_cards += 3
    assert res['status'] == 'ended' and out_cards > 60
    leave()

