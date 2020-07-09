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
        """
        Метод разбирает строку данных от клиента по ключевым
        словам и перенаправляет в соответствующе модули
        для дальнейшей обработки. Ответом является ответ
        соответвующий ключу словаря ответов сервера
        '200'...'400'
        :param request: строка запроса от клиента
        :return: ключ словаря ответов сервера
        """
        if request["action"] == "authenticate":
            logger.debug(f'Для авторизации подготовлены данные {request["user"]}')
            local_status = self.autenticate(f=request["user"])
            if local_status == "200" or local_status == "201":
                self.status = "authenticate"
            logger.debug(f'Проверка установили статус {local_status}')
            server_answer_json = server_answer[f'{local_status}']
            self.token = server_answer_json["token"]
        else:
            server_answer_json = server_answer["400"]
        return server_answer_json

    def autenticate(self, f):

        """
        Метод авторизации клиентов.
        В созданный объект класса User
        зановистся имя, пороль и токен авторизации.
        :param f: строка словаря запросов клиента.
        :return: кортеж имя/пароль зарегистрированного пользователя.
        """
        user_attr = (f["account_name"], f["password"])
        logger.debug(f'атрибуты для регистрации {user_attr}')
        server_answer = save_user(user_attr)
        print(f'После проверки статус {server_answer}')
        return server_answer

    def connection_token(self, start_token):
        """Cоздание токена подключенного и авторизованного клиента."""
        if start_token == "":
            start_token = f'{datetime.now()}_auth'
            logger.debug(f'Выдан токен {start_token}')
            return start_token


# Декоратор логирования
def log(logger):
    """
    Добавляет логирование ответов сервера и запросов
    клиента для режима DEBUG
    :param logger: экземляр класса логгера для вывода строк логирования
    :return: возвращает функци со строками логирования
    """
    def actual_decorator(fn):
        def wrapper(*args, **kwargs):
            fn_result = fn(*args, **kwargs)
            logger.debug(f'Строка для преобразования'
                         f'{fn_result}')
            return fn_result
        return wrapper
    return actual_decorator


def processing_client_request(client_data):
    """
    Обрабатывает ответ сервера и преобразует его
    в словарь ответа сервера клиенту, взятый из шаблона
    ответов сервера.
    :param client_data:
    :return:
    """
    if client_data["action"] == "authenticate":
        user = User()
        logger.debug(f'создан пользователь {user.account_name}')
        return user
    elif client_data["action"] == "msg":
        answer = server_answer["200"]
        answer["alert"] = "Ваше сообщение принято"
        return answer


@log(logger=logging.getLogger('server'))
def client_server_answer(BUFSIZE):
    logger.info('Получение данных клиента и декодирование их')
    data = client_socket.recv(BUFSIZE).decode('utf-8')
    return data


@log(logger=logging.getLogger('server'))
def json_dump_data(string_data):
    logger.info('Сохранение данных в JSON строку для отпаравки на клиента')
    json_data = json.dumps(string_data, ensure_ascii=False).encode('utf-8')
    return json_data


@log(logger=logging.getLogger('server'))
def json_load_data(string):
    logger.info('Загрузка декодированных Json данных от клиента')
    json_string = json.loads(string, encoding="utf-8")
    return json_string


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
        data = client_server_answer(BUFSIZE)
        # Битовая срока преобразуется в словарь
        if data == "":
            pass
        else:
            client_data = json_load_data(data)
            if client_data["action"] == "authenticate":
                user = processing_client_request(client_data)
            processing_client_request(client_data)
        # client_data = json.loads(client_socket.recv(BUFSIZE).decode('utf-8'))
        # раскодированная строка отправляется
        # в функцию класса User на разбор запроса клиента
        client_data = user.parser(client_data)
        # Полученная с разбора строка выгружается в строку
        # json для последующиего отправления через сокет
        logger.debug(f'Отправленные данные клиенту {client_data}')
        data = json_dump_data(client_data)
        # отправка битовой строки ответа клиенту
        client_socket.send(data)

    # закрытие сокета после отключения
    client_socket.close()
    logger.debug('Приложение клиента отключилось')
    break
server_socket.close()


