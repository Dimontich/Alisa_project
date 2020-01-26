from alice_code import get_random_card, first_step, parse_card, get_new_random_card, alice_turn, player_turn


def test_wrong_input():
    """Проверка ввода ерунды"""
    # TODO
    pass


def test_get_random_card():
    """Проверка получения случайной карты"""

    assert get_random_card(['1c']) == '1c'


def test_first_step():
    """Проверка первого шага"""

    data = dict()
    first_step(data)

    assert data['is_player_turn'] != None
    assert data['alice_data'] != None
    assert data['player_data'] != None
    assert data['cards'] != None
    assert data['is_end'] is False

    assert data['alice_data']['card_list'][0] not in data['cards']
    assert data['alice_data']['card_list'][1] not in data['cards']
    assert data['alice_data']['card_list'][2] not in data['cards']
    assert data['player_data']['card_list'][0] not in data['cards']
    assert data['player_data']['card_list'][1] not in data['cards']
    assert data['player_data']['card_list'][2] not in data['cards']


def test_parse_card():
    """Проверка парса названия карты"""

    assert parse_card('8j')[0] == 8
    assert parse_card('8j')[1] == 'j'


def test_get_new_random_card_available():
    """Проверка взятия карты из колоды"""

    data = dict(cards=['1a', '1b'],
                player_data=dict(card_list=[]),
                alice_data=dict(card_list=[]))

    result = get_new_random_card(data, True)
    assert result is True

    assert len(data['cards']) == 1
    assert len(data['player_data']['card_list']) == 1
    assert len(data['alice_data']['card_list']) == 0

    result = get_new_random_card(data, False)
    assert result is True

    assert len(data['cards']) == 0
    assert len(data['player_data']['card_list']) == 1
    assert len(data['alice_data']['card_list']) == 1


def test_get_new_random_card_bad():
    """Проверка взятия карты из колоды (в колоде карт нет)"""

    data = dict(cards=[],
                player_data=dict(card_list=[]),
                alice_data=dict(card_list=[]))

    assert get_new_random_card(data, True) is False


def test_alice_turn_good():
    """Ход Алисы. На столе есть карта, есть бита в руке.
    Ожидается, что Алиса побьет карту на столе и положит новую"""

    data = dict(current_card='3c',
                alice_data=dict(card_list=['5d',
                                           '9k',
                                           '4c']),
                # player_data=dict(),
                is_player_turn=False,
                cards=['1a'],
                is_end=False)

    alice_turn(data)

    assert data['current_card'] != None  # На столе есть карта
    assert len(data['alice_data']['card_list']) == 2  # Количество карт в руке 2 (бита, взяла, положила)
    assert '4c' not in data['alice_data']['card_list']  # Карта для биты не в руке
    assert len(data['cards']) == 0  # В колоде больше нет карт
    assert data['is_player_turn'] is True  # Ход передан игроку

    assert data['is_end'] is False  # Игра не окончена


def test_alice_turn_bad():
    """Ход Алисы. На столе есть карта, нет биты в руке.
    Ожидается, что Алиса побьет карту на столе и положит новую"""

    data = dict(current_card='3c',
                alice_data=dict(card_list=['5d',
                                           '9k']),
                # player_data=dict(),
                is_player_turn=False,
                cards=['1a'],
                is_end=False)

    alice_turn(data)

    assert data['current_card'] == None  # На столе нет карты
    assert len(data['alice_data']['card_list']) == 3  # Количество карт в руке 3 (взято со стола)
    assert '3c' in data['alice_data']['card_list']  # Карта со стола в руке
    assert len(data['cards']) == 1  # В колоде осталась карта
    assert data['is_player_turn'] is True  # Ход передан игроку

    assert data['is_end'] is False  # Игра не окончена


def test_alice_turn_no_current_card():
    """Ход Алисы. На столе нет карты. В руке 2 карты
    Ожидается, что Алиса возьмет карту из колоды и положит карту из руки на стол"""

    data = dict(current_card=None,
                alice_data=dict(card_list=['5d',
                                           '9k']),
                # player_data=dict(),
                is_player_turn=False,
                cards=['1a'],
                is_end=False)

    alice_turn(data)

    assert data['current_card'] != None  # На столе нет карты
    assert len(data['alice_data']['card_list']) == 2  # Количество карт в руке 2
    assert data['current_card'] not in data['alice_data']['card_list']  # Карты со стола нет в руке
    assert len(data['cards']) == 0  # В колоде осталась карта
    assert data['is_player_turn'] is True  # Ход передан игроку

    assert data['is_end'] is False  # Игра не окончена


def test_alice_turn_win():
    """Ход Алисы. На столе нет карты. В руке нет карт, в колоде нет карт"""

    data = dict(current_card=None,
                alice_data=dict(card_list=[]),
                # player_data=dict(),
                is_player_turn=False,
                cards=[],
                is_end=False)

    answer = alice_turn(data)

    assert 'выигр' in answer

    assert data['current_card'] is None  # На столе нет карты
    assert len(data['alice_data']['card_list']) == 0  # Количество карт в руке 0
    assert len(data['cards']) == 0  # В колоде осталась карта

    assert data['is_end'] is True  # Игра окончена


def test_player_turn_good():
    """Ход игрока. На столе есть карта, игрок отбивает"""

    data = dict(current_card='1a',
                player_data=dict(card_list=['5d',
                                            '9k',
                                            '5a']),
                is_player_turn=True,
                cards=[],
                is_end=False)

    player_turn('5a', data)

    assert data['current_card'] is None  # Бита
    assert len(data['player_data']['card_list']) == 2
    assert data['is_player_turn'] is True  # Еще раз ходит игрок
    assert data['is_end'] is False


def test_player_turn_good_add_card():
    """Ход игрока. На столе есть карта, игрок отбивает и берет карту из колоды"""

    data = dict(current_card='1a',
                player_data=dict(card_list=['5d',
                                            '9k',
                                            '5a']),
                is_player_turn=True,
                cards=['6h'],
                is_end=False)

    player_turn('5a', data)

    assert data['current_card'] is None  # Бита
    assert len(data['player_data']['card_list']) == 3
    assert data['is_player_turn'] is True  # Еще раз ходит игрок
    assert data['is_end'] is False
    assert len(data['cards']) == 0


def test_player_turn_place():
    """Ход игрока. На столе нет карты, игрок кладет карту и берет карту из колоды"""

    data = dict(current_card=None,
                player_data=dict(card_list=['5d',
                                            '9k',
                                            '5a']),
                is_player_turn=True,
                cards=[],
                is_end=False)

    player_turn('9k', data)

    assert data['current_card'] == '9k'  # На столе есть карта
    assert len(data['player_data']['card_list']) == 2
    assert data['is_player_turn'] is False  # Ходит Алиса
    assert data['is_end'] is False


def test_player_turn_place_add_card():
    """Ход игрока. На столе нет карты, игрок кладет карту и берет карту из колоды"""

    data = dict(current_card=None,
                player_data=dict(card_list=['5d',
                                            '9k',
                                            '5a']),
                is_player_turn=True,
                cards=['6h'],
                is_end=False)

    player_turn('9k', data)

    assert data['current_card'] == '9k'  # На столе есть карта
    assert len(data['player_data']['card_list']) == 3  # Еще карту взяли из колоды
    assert data['is_player_turn'] is False  # Ходит Алиса
    assert data['is_end'] is False
    assert len(data['cards']) == 0  # Колода пустая
