"""Unit-тесты сервера."""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from lesson7.server.server import processing_client_request


class TestClass(unittest.TestCase):
    """Класс с тестами."""

    def test_authorization_user(self):
        client_data = {'action': 'msg', 'status': 'authenticate', 'time': '01/07/20 18:50:08',
                       'user': {'account_name': 'Жоржик', 'password': 'коржик'}}
        self.assertEqual(processing_client_request(client_data) == {"response": 200, "alert": "Ваше сообщение принято"})

