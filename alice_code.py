## @package alice_code
## @brief Файл с логикой Алисы

import random

from alice_class import AliceResponse, AliceRequest

## Текст приветствия
HELLO_TEXT = """Добро пожаловать в игру матстак. 
Каждому игроку в начале раздается по три карты.

Доступные команды:
Начать - начать игру
Беру - взять карту со стола
/карта/ - положить карту из руки на стол
"""

## Список всех карт
ALL_CARDS = ["1a", "2a", "3a", "4a", "5a", "6a",
             "1b", "2b", "3b", "4b", "5b", "6b",
             "1c", "2c", "3c", "4c", "5c", "6c",
             "1d", "2d", "3d", "4d", "5d", "6d"]


# ALL_CARDS = ["1a", "2a", "3a", "4a", "5a", "6a", ]


## Выделяет из карты номер и масть
## @param text Название карты
## @return Кортеж из номера и масти
def parse_card(text):
    return (int(text[0]),
            text[1])


## Функция, координирующая действия бизнес-логики
## @param request Объект запроса
## @param response Объект ответа
## @param session_data Информация о сессии
## @return Новая информация о сессии
def handle_dialog(request: AliceRequest, response: AliceResponse, session_data: dict):
    is_zero_game = len(session_data) == 0
    if is_zero_game:
        session_data['is_end'] = True
        response.set_text(HELLO_TEXT)
        return session_data

    command = request.command
    if session_data['is_end']:
        if command.lower() == 'начать':
            first_step(session_data)

            answer = alice_turn(session_data)
            response.set_text(answer)
            response.append_text(f'Карты в руке: {session_data["player_data"]["card_list"]}')

        else:
            response.set_text('Игра окончена. Чтобы начать, введите "Начать"')

        return session_data

    if command.lower() == 'фалалеев':
        response.set_text(f'Читерить плохо!\n'
                          f'Карты в колоде: {session_data["cards"]}\n'
                          f'Карты в руке Алисы: {session_data["alice_data"]["card_list"]}')

        return session_data

    if session_data['is_player_turn']:
        if command.lower() == 'беру':
            if session_data['current_card'] is None:
                response.set_text('На столе нет карт')
                return session_data

            card = session_data['current_card']
            session_data['player_data']['card_list'].append(card)
            session_data['current_card'] = None

            session_data['is_player_turn'] = False

            response.set_text(f'Вы взяли карту {card}\n')

        elif len(command) != 2:
            response.set_text(f'Команда {command} отсутствует\n')

        else:
            answer = player_turn(command, session_data)
            response.set_text(answer)

        if not session_data['is_player_turn']:
            response.append_text(alice_turn(session_data))
            response.append_text(f'Карты в руке: {session_data["player_data"]["card_list"]}\n')

    else:
        # ходит Алиса
        # А почему она ходит: 0_0
        response.set_text('Ой все\n')

    card_list = session_data['player_data']['card_list']  # Карты в руке
    if len(card_list) == 0 and len(session_data['cards']) == 0:
        response.append_text(f'Вы выиграли. \nНапишите "Начать", чтобы начать заного\n')

    return session_data


## Получить случайную карту
## @param card_list Списки с картами
## @return Карта (название)
def get_random_card(card_list):
    return card_list[random.randint(0, len(card_list) - 1)]


## Инициализация игрока и Алисы
## @param session_data Данные о сессии
def first_step(session_data):
    session_data['is_player_turn'] = False  # True - если ход игрока, иначе - ход Алисы
    session_data['alice_data'] = dict()  # Данные об Алиса
    session_data['player_data'] = dict()  # Данные об игроке
    session_data['cards'] = ALL_CARDS.copy()  # Доступные карты
    session_data['current_card'] = None  # Карта на столе
    session_data['is_end'] = False

    # Карты для Алисы и игрока
    for data in (session_data['alice_data'], session_data['player_data']):  # берем по ссылке данные
        data['card_list'] = []

        for i in range(0, 3):
            card = get_random_card(session_data['cards'])

            data['card_list'].append(card)
            session_data['cards'].remove(card)


## Получить новую случайную карту
## @param session_data Данные о сессии
## @param is_player_turn True, если карту берет игрок, иначе - карту берет Алиса
## @return True, если операция успешна, иначе - False
def get_new_random_card(session_data, is_player_turn):
    if len(session_data['cards']) == 0:
        return False

    card = get_random_card(session_data['cards'])

    data = session_data['player_data'] if is_player_turn else session_data['alice_data']

    data['card_list'].append(card)
    session_data['cards'].remove(card)

    return True


## Логика хода игрока
## @param card_name Карта
## @param session_data Информация о сессии
## @return Текст ответа
def player_turn(card_name, session_data):
    answer = ''
    card_list = session_data['player_data']['card_list']  # Карты в руке

    if card_name not in card_list:
        return f'В руке нет такой карты. Доступные карты: {str(card_list)}\n'

    # На столе есть карта
    if session_data['current_card']:
        player_number, player_type = parse_card(card_name)
        table_number, table_type = parse_card(session_data['current_card'])

        if player_type != table_type:
            return f'Масть карты на столе ({session_data["current_card"]}) не совпадает с Вашей картой ({card_name})\n'

        if player_number <= table_number:
            return f'Вы не можете побить карту на столе ({session_data["current_card"]}) ' \
                   f'Вашей картой меньшего веса ({card_name})\n'

        session_data['current_card'] = None
        card_list.remove(card_name)

        # Берем карту из колоды, если нужно
        if len(card_list) < 3:
            if get_new_random_card(session_data, True):
                answer += 'Вы взяли карту из колоды\n'

        return answer + f'Бита. \nПоложите карту на стол. Карты в руке: {str(card_list)}\n'

    # Надо положить карту на стол
    session_data['current_card'] = card_name

    session_data['player_data']['card_list'].remove(card_name)
    session_data['is_player_turn'] = False

    # Берем карту из колоды, если нужно
    if len(card_list) < 3:
        if get_new_random_card(session_data, True):
            answer += 'Вы взяли карту из колоды\n'

    return f'Вы положили на стол карту {card_name}\n' \
           f'Карты в руке: {str(card_list)}\n'


## Логика хода Алисы
## @param session_data Информация о сессии
## @return Ответ
def alice_turn(session_data):
    answer = ''

    if session_data['current_card']:
        table_number, table_type = parse_card(session_data['current_card'])

        for card in session_data['alice_data']['card_list']:
            alice_number, alice_type = parse_card(card)

            if alice_type == table_type and alice_number > table_number:
                session_data['current_card'] = None
                session_data['alice_data']['card_list'].remove(card)

                answer += 'Бита\n'
                break

        # Отбить не удалось
        if session_data['current_card']:
            session_data['alice_data']['card_list'].append(session_data['current_card'])
            session_data['current_card'] = None

            session_data['is_player_turn'] = True

            answer += 'Беру. Положите карту на стол\n'

    # Алиса кладет карту
    if not session_data['is_player_turn']:
        card_list = session_data['alice_data']['card_list']
        if len(card_list) < 3:
            get_new_random_card(session_data, False)

        if len(card_list) == 0:
            session_data['is_end'] = True
            return f'Я выиграла\n'

        card = get_random_card(card_list)  # Достаем случайную карту из руки

        card_list.remove(card)  # Убираем из руки
        session_data['current_card'] = card  # Кладем на стол

        session_data['is_player_turn'] = True

        answer += f'Положила на стол {session_data["current_card"]}\n'
        answer += f'Ваш ход\n'

    return answer
