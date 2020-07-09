import unittest
from lesson03.server.server import User


def test_authorization_user():
    user = User
    client_data = {'action': 'authenticate', 'status': 'no_authenticate', 'time': '01/07/20 18:50:08', 'user': {'account_name': 'Жоржик', 'password': 'коржик'}}
    assert user.parser(user=user, request=client_data) == {"response": 201, "alert": "Создана новая учетная запись"}


def test_authorization_user():
    user = User
    client_data = {'action': 'authenticate', 'status': 'no_authenticate', 'time': '01/07/20 18:50:08', 'user': {'account_name': 'Жоржик', 'password': 'коржик'}}
    assert user.parser(user=user, request=client_data) == {"response": 200, "alert": "Необязательное сообщение/уведомление"}


