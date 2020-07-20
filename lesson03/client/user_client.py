from lesson03.client.util_tools import action
from datetime import datetime
import logging
import lesson03.client.client_log_config


class User(object):
    """class user tcp_client."""
    def __init__(self, name="noname", login="", status=False,
                 action=action, time_create=datetime.today().strftime("%d/%m/%y %H:%M:%S"), token=""):

        """
        create on load app
        :param name: name user`s app
        :param login: login user`s app
        """
        self.name = name
        self.login = login
        self.status = status is bool
        self.action = action
        self.time_create = time_create
        self.token = token

        self.action["authenticate"]["time"] = self.time_create

    def autenticate(self):
        """
        Подставляет в json запрос action
        пару "account_name"/"password"
        :return: - запрос "authenticate""

        """
        if not self.status:
            self.action["authenticate"]["user"]["account_name"] = \
                str(input("Введите ваш ник, до 6 символов"))
            self.action["authenticate"]["user"]["password"] = \
                str(input("Введите ваш пароль"))
            data = self.action["authenticate"]

        return data

    def msg(self, request):
        """Получает строку запроса вставляет ее в поле
        "msg" - словаря action
        и возвращает измененный словарь для отправки на сервер.
        ---- Пока в разработке---
        """
        self.action["msg"]["token"] = request["token"]
        return self.action["msg"]

    def set_change(self, data):
        """
        Сохраняет изменения клиентского
        профиля после обмена сообщениями с
        сервером.
        """
        self.token = data["token"]
        self.name = self.action["authenticate"]["user"]["account_name"]


