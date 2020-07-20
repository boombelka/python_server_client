from socket import AF_INET, SOCK_STREAM, socket
from lesson7.server.util_server_tools import server_answer
from lesson7.server.servconf import ADDR, BUFSIZE, SERV_LISTEN
import json
from datetime import datetime
from lesson7.server.util_server_tools import save_user
import logging
import select
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
        logger = logging.getLogger('server')
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
        # logger = logging.getLogger('server')
        user_attr = (f["account_name"], f["password"])
        # logger.debug(f'атрибуты для регистрации {user_attr}')
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
            logger.info(f'Отрабатывает функция {fn.__name__}')
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
    # logger = logging.getLogger('server')
    if client_data["action"] == "authenticate":
        user = User()
        # logger.debug(f'создан пользователь {user.account_name}')
        return user
    elif client_data["action"] == "msg":
        answer = server_answer["200"]
        answer["alert"] = "Ваше сообщение принято"
        return answer
    elif client_data['users']:
        pass


@log(logger=logging.getLogger('server'))
def client_server_answer(BUFSIZE):
    logger = logging.getLogger('server')
    logger.info('Получение данных клиента и декодирование их')
    data = client_socket.recv(BUFSIZE).decode('utf-8')
    return data


@log(logger=logging.getLogger('server'))
def json_dump_data(string_data):
    logger = logging.getLogger('server')
    logger.info('Сохранение данных в JSON строку для отпаравки на клиента')
    json_data = json.dumps(string_data, ensure_ascii=False)
    return json_data


@log(logger=logging.getLogger('server'))
def json_load_data(string):
    logger = logging.getLogger('server')
    logger.info('Загрузка декодированных Json данных от клиента')
    json_string = json.loads(string, encoding="utf-8")
    return json_string


def read_requests(r_clients, all_clients):
    """Чтение запросов из списка клиентов."""
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}
    logger = logging.getLogger('server')
    for sock in r_clients:
        try:
            data = sock.recv(1024).decode('utf-8')
            print(f'строк для разбора пришедшая от клиента {data}')
            client_data = json_load_data(data)
            print(f'строк после выгрузки из JSON {client_data}')
            if client_data == "":
                print(f'Пришла строка {client_data}')
            elif client_data["action"] == "authenticate":
                user = processing_client_request(client_data)
            elif client_data['users']:
                pass

            processing_client_request(client_data)
            # client_data = json.loads(client_socket.recv(BUFSIZE).
            # decode('utf-8'))
            # раскодированная строка отправляется
            # в функцию класса User на разбор запроса клиента
            client_data = user.parser(client_data)
            # Полученная с разбора строка выгружается в строку
            # json для последующиего отправления через сокет
            logger.debug(f'Отправленные данные клиенту {client_data}')
            data = json_dump_data(client_data)
            logger.debug(f'данные возвращенные функцией json_dump_data {data}')
            responses[sock] = data
            logger.debug(f'Словарь {responses}')
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(),
                                                   sock.getpeername()))
            logger.debug(f'Клиент {sock.fileno()} - {sock.getpeername()}'
                         f' отключился')
            all_clients.remove(sock)

#    logger.debug(f'Функция responses закончила свою работу')
    print(responses)
    return responses


def write_responses(responses, w_clients, all_clients):
    """Эхо-ответ сервера клиентам, от которых были запросы."""
    for sock in w_clients:
        if sock in responses:
            try:
                # Подготовить и отправить ответ сервера
                resp = responses[sock].encode('utf-8')
                # Эхо-ответ сделаем чуть непохожим на оригинал
                test_len = sock.send(resp)
            except:  # Сокет недоступен, клиент отключился
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


def mainloop():
    """Основной цикл обработки запросов клиентов."""
    logger = logging.getLogger('server')
    clients = []

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(ADDR)
    s.listen(5)
    s.settimeout(1.0)  # Таймаут для операций с сокетом
    logger.debug(f'загружены параметры подключений к сокету - {ADDR}, {SERV_LISTEN}')
    while True:
        try:
            conn, addr = s.accept()  # Проверка подключений
            logger.debug('Сокет запущен на прослушивание')
        except OSError as e:
            pass  # timeout вышел
        else:
            print('Получен запрос на соединение от %s' % str(addr))
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 0
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass  # Ничего не делать, если какой-то клиент отключился

            responses = read_requests(r, clients)  # Сохраним запросы клиентов
            print(responses)
            print(clients)
 #          logger.debug(f'список подсоединеных клиентов {responses}')
            write_answer = write_responses(responses, w, clients)  # Выполним отправку ответов клиентам
 #           logger.debug(f'Закончена отправка сообщений клиентам {write_answer}')

mainloop()
