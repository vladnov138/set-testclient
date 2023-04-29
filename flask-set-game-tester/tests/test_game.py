import json
from modules.connection_utils.connection_utils import leave
from modules.connection_utils.connection_utils import create_room
from modules.connection_utils.connection_utils import get_gamelist
from modules.connection_utils.connection_utils import add_cards
from modules.connection_utils.connection_utils import get_field
from modules.connection_utils.connection_utils import pick
from modules.connection_utils.connection_utils import select_three_cards
from modules.connection_utils.connection_utils import is_set
from modules.connection_utils.connection_utils import check_response

USER_FILE_ONE = '../userdata_1.json'
USER_FILE_TWO = '../userdata_2.json'


def get_userdata_fjson(jsonfile: str):
    with open(jsonfile, "r") as f:
        data = json.load(f)
        return data["nickname"], data["token"]


USER1_NAME, USER1_TOKEN = get_userdata_fjson(USER_FILE_ONE)
USER2_NAME, USER2_TOKEN = get_userdata_fjson(USER_FILE_TWO)


def test_creating_room():
    leave(USER1_TOKEN)
    res = create_room(USER1_TOKEN)
    check_response(res, success=True, exception=None, gameId=None)
    res = create_room(USER1_TOKEN)
    check_response(res, success=False, exception=None)
    leave(USER1_TOKEN)


def test_list_room():
    leave(USER1_TOKEN)
    res = get_gamelist(USER1_TOKEN)
    check_response(res, success=True, exception=None, games=None)
    assert len(res['games']) >= 0


def test_cards():
    leave(USER1_TOKEN)
    create_room(USER1_TOKEN)
    res = get_field(USER1_TOKEN)
    check_response(res, success=True, exception=None, fieldCards=None)
    card = res['fieldCards'][11]
    check_response(card, count=None, color=None, fill=None, shape=None)


def test_room():
    leave(USER1_TOKEN)
    leave(token=USER2_TOKEN)

    res = get_gamelist(token=USER2_TOKEN)
    check_response(res, success=True, exception=None, games=None)
    count_games = len(res['games'])

    game_id = create_room(USER1_TOKEN)['gameId']

    res = get_gamelist(token=USER2_TOKEN)
    check_response(res, success=True, exception=None, games=None)
    new_count_games = len(res['games'])

    assert new_count_games > count_games
    count_games = new_count_games

    res = send_request('/set/room/enter', accessToken=USER2_TOKEN, gameId=game_id)
    check_response(res, success=True, exception=None, gameId=None)

    res = leave(token=USER2_TOKEN)
    check_response(res, success=True, exception=None)
    res = leave(token=USER1_TOKEN)
    check_response(res, success=False, exception=None)
    res = leave(USER1_TOKEN)
    check_response(res, success=True, exception=None)

    res = get_gamelist(token=USER2_TOKEN)
    check_response(res, success=True, exception=None, games=None)
    new_count_games = len(res['games'])

    assert new_count_games < count_games


def test_field():
    leave(USER1_TOKEN)
    res = get_field(USER1_TOKEN)
    check_response(res, success=False, exception=None)
    create_room(USER1_TOKEN)
    res = get_field(USER1_TOKEN)
    check_response(res, success=True, exception=None, fieldCards=None, status='ongoing')
    cards = res['fieldCards']
    assert len(cards) == 12
    leave(USER1_TOKEN)


def test_add():
    leave(USER1_TOKEN)
    res = add_cards(USER1_TOKEN)
    check_response(res, success=False, exception=None)

    create_room(USER1_TOKEN)
    cards = get_field(USER1_TOKEN)['fieldCards']
    cur_len = len(cards)
    while cur_len < 21:
        res = add_cards(USER1_TOKEN)
        check_response(res, success=True, exception=None)
        cur_cards = get_field(USER1_TOKEN)['fieldCards']
        cur_len += 3
        assert cur_len == len(cur_cards)
    res = add_cards(USER1_TOKEN)
    check_response(res, success=False, exception=None)
    leave(USER1_TOKEN)


def test_pick():
    leave(USER1_TOKEN)
    res = pick([1, 2, 3], USER1_TOKEN)
    check_response(res, success=False, exception=None)

    create_room(USER1_TOKEN)
    res = get_field(USER1_TOKEN)
    cards = res['fieldCards']
    chosen_cards = select_three_cards(cards)
    while len(chosen_cards) == 0:
        add_cards(USER1_TOKEN)
        cards = res['fieldCards']
        chosen_cards = select_three_cards(cards)
    res = pick(chosen_cards, USER1_TOKEN)
    check_response(res, success=True, exception=None, isSet=True)
    new_res = get_field(USER1_TOKEN)
    new_len = len(new_res['fieldCards'])

    assert 12 <= new_len <= 21

    res = pick(chosen_cards, USER1_TOKEN)
    check_response(res, success=False, exception=None)

    cards = get_field(USER1_TOKEN)['fieldCards']
    chosen_cards = select_three_cards(cards, set=False)
    res = pick(chosen_cards, USER1_TOKEN)
    check_response(res, success=True, exception=None, isSet=False)
    leave(USER1_TOKEN)


def test_score():
    leave(USER1_TOKEN)
    create_room(USER1_TOKEN)
    res = send_request('/set/score', accessToken=USER1_TOKEN)
    check_response(res, success=True, exception=None, users=None)
    old_score = res['users'][0]['score']
    cards = get_field(USER1_TOKEN)['fieldCards']
    pick(select_three_cards(cards), USER1_TOKEN)
    res = send_request('/set/score', accessToken=USER1_TOKEN)
    check_response(res, success=True, exception=None, users=None)
    new_score = res['users'][0]['score']
    assert new_score > old_score


def test_imitate_game():
    leave(USER1_TOKEN)
    create_room(USER1_TOKEN)
    out_cards = 0
    status = 'ongoing'
    cards = get_field(USER1_TOKEN)['fieldCards']
    while out_cards < 81 and status == 'ongoing':
        chosen_cards = select_three_cards(cards, set=False)
        res = pick(chosen_cards, USER1_TOKEN)
        check_response(res, success=True, exception=None, isSet=False)

        chosen_cards = select_three_cards(cards)
        while len(chosen_cards) == 0:
            add_cards(USER1_TOKEN)
            cards = get_field(USER1_TOKEN)['fieldCards']
            chosen_cards = select_three_cards(cards)
        res = pick(chosen_cards, USER1_TOKEN)
        check_response(res, success=True, exception=None, isSet=True)

        status = get_field(USER1_TOKEN)['status']
        cards = get_field(USER1_TOKEN)['fieldCards']
        out_cards += 3
    assert status == 'ended' and out_cards > 60
    leave(USER1_TOKEN)


