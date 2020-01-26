##@package main
# Файл с реализацией flask-приложения

from __future__ import unicode_literals

import json
import logging

from flask import Flask, request

from alice_class import AliceRequest, AliceResponse
from alice_code import handle_dialog

app = Flask(__name__)

session_storage = {}

with open("sessions.json", "w", encoding="utf8") as file:
    json.dump(session_storage, fp=file)


@app.route("/", methods=["POST"])
## Основная функция
# Функция для взаимодействия между пользователем и сайтом
# @return   Функция получает тело запроса и возвращает ответ
def main():
    with open("sessions.json", encoding="utf8") as session_file:
        session_storage = json.loads(session_file.read())

    alice_request = AliceRequest(request.json)

    alice_response = AliceResponse(alice_request)

    user_id = alice_request.user_id

    session_storage[user_id] = handle_dialog(alice_request,
                                             alice_response,
                                             session_storage.get(user_id,
                                                                 dict()))

    # Потому что оперативка плохо работает
    with open("sessions.json", "w", encoding="utf8") as session_file:
        json.dump(session_storage, fp=session_file)

    logging.info("Response: {}".format(alice_response))

    return alice_response.dumps()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
