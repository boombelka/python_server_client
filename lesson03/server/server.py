from socket import AF_INET, SOCK_STREAM, socket
from lesson03.server.util_server_tools import server_answer
from lesson03.server.servconf import ADDR, BUFSIZE, SERV_LISTEN
import json
from datetime import datetime
from lesson03.server.util_server_tools import save_user
import logging
import lesson03.server.server_log_config


"""
Коммуникационная часть сервера месенджера
"""


class User:
    """
    Класс пользователя.
    Создается при подключении и работает с клиентом при всем
    времени его работы с сервером.
    """

    def __init__(self, account_name='noname',
                 status='not_authenticate', password='No', token=""):
        """
        Инициализация класса.
        :param account_name: - имя пользователя.
        :param status: - статус пользователя (авторизован, не_авторизован).
        :param password: - пароль пользователя.
        """
        self.account_name = account_name
        self.status = status
        self.password = password
        self.token = token

    def parser(self, request):
        if request["action"] == "authenticate":
            if request["status"] == "no_authenticate":
                logger.debug(f'Для авторизации подготовлены данные {request["user"]}')
                local_status = self.autenticate(f=request["user"])
                if local_status == "200" or local_status == "201":
                    self.status = "authenticate"
                logger.debug(f'Проверка установили статус {local_status}')
                server_answer_json = server_answer[f'{local_status}']
                self.token = server_answer_json["token"]

                return server_answer_json

    def autenticate(self, f):
        user_attr = (f["account_name"], f["password"])
        logger.debug(f'атрибуты для регистрации {user_attr}')
        server_answer = save_user(user_attr)
        print(f'После проверки статус {server_answer}')
        return server_answer

    def connection_token(self, start_token):
        if start_token == "":
            start_token = f'{datetime.now()}_auth'
            logger.debug(f'Выдан токен {start_token}')
            return start_token


# определение необходимых параметров:
# определение экземпляра логера.
logger = logging.getLogger('server')
# запуск сокета с параметрами.
server_socket = socket(AF_INET, SOCK_STREAM)
# определение порта и адреса для работы сокета
server_socket.bind(ADDR)
# определение максимального количества
# соединений в очереди до вызова
# функции accept
server_socket.listen(SERV_LISTEN)
logger.debug(f'загружены параметры подключений к сокету - {ADDR}, {SERV_LISTEN}')
user = User()
logger.debug(f'создан пользователь {user.account_name}')

while True:
    print('witing.....')
    # Определение сокета и адреса (ip, port) подключения к серверу
    client_socket, addr = server_socket.accept()
    logger.debug('Сокет запущен на прослушивание')
    print(f'connected from: {addr}')
    # На 1 подключение создается объект подключения
    # в котором храняться данные подключения

    while True:
        # Сервер получает запрос с клиента и
        # декодирует его из битовогоформата в
        # строку json
        data = client_socket.recv(BUFSIZE).decode('utf-8')
        # Битовая срока преобразуется в словарь
        client_data = json.loads(data, encoding="utf-8")
        # client_data = json.loads(client_socket.recv(BUFSIZE).decode('utf-8'))
        # раскодированная строка отправляется
        # в функцию класса User на разбор
        client_data = user.parser(request=client_data)
        # Полученная с разбора строка выгружается в строку
        # json для последующиего отправления через сокет
        logger.debug(f'Отправленные данные клиенту {client_data}')
        data = json.dumps(client_data, ensure_ascii=False).encode('utf-8')
        # отправка битовой строки ответа клиенту
        client_socket.send(data)
        input("введите что нибудь")

    # закрытие сокета после отключения
    client_socket.close()
    logger.debug('Приложение клиента отключилось')
    break
server_socket.close()


