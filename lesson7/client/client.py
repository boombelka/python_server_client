"""Клиентская часть приложения."""
from lesson7.client.cliconf import ADDR, BUFSIZE
from socket import AF_INET, SOCK_STREAM, socket
import json
from lesson7.client.user_client import User
import datetime
import logging
import select
import sys
import lesson03.client.client_log_config
# не разобрался - убираешь - не работает


# Декоратор логирования
def log(logger):
    def actual_decorator(fn):
        def wrapper(*args, **kwargs):
            fn_result = fn(*args, **kwargs)
            logger.debug(f'Строка для преобразования'
                         f'{fn_result}')
            logger.debug(f'Создание соединения: {time_create}')
            logger.info(f'Отрабатывает функция {fn.__name__}')
            return fn_result
        return wrapper
    return actual_decorator


@log(logger=logging.getLogger('client'))
def json_dump_data(string):
    logger.info(f'Преобразование строки данных для отправки на сервер. {string}')
    data = json.dumps(string, ensure_ascii=False).encode('utf-8')
    logger.info(f'{data}')
    return data


@log(logger=logging.getLogger('client'))
def json_load_data(b_data):
    logger.info(f'Преобразование результата ответа сервереа')
    data = json.loads(b_data, encoding="utf-8")
    return data


@log(logger=logging.getLogger('client'))
def client_server_answer(BUFSIZE):
    logger.info('Получение запроса клиента к серверу')
    server_answer = sock.recv(1024).decode('utf-8')
    logger.info(f'Получен от сервера ответ {server_answer}')
    return server_answer


@log(logger=logging.getLogger('client'))
def client_server_send(string_data):
    logger.info(f'Отправление запроса клиента серверу {string_data}')
    sock.send(string_data)


# Начиная с Python 3.2 сокеты имеют протокол менеджера контекста
# При выходе из оператора with сокет будет авторматически закрыт
logger = logging.getLogger('client')
time_create = datetime.datetime.today().strftime("%d/%m/%y %H:%M:%S")
user = User()
print(user.name)
logger.debug(f'создан пользователь с именем {user.name}.')

with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
    sock.connect(ADDR)  # Соединиться с сервером

    while True:
        if user.name == "noname":
            # Первоначальная регистрация пользователя
            user.autenticate()
            string = user.action["authenticate"]
            # Импорт запроса в JSON строку.
            data = json_dump_data(string)
            # Отправка запроса авторизации серверу.
            client_server_send(data)
            # Получение ответа от сервера
            data = client_server_answer(BUFSIZE)
            logger.debug(f'Получен ответ от сервера,,, {data}')
            # Преобразование ответа из json строки в словарь.
            data = json_load_data(data)

            user_set_change = user.set_change(data)
            logger.debug(f'Пользователь получил токен '
                         f'{user.token} и имя {user.name}')
            print(data['alert'])
        else:
            user_action = str(input('Введите запрос'))
            if user_action == "authenticate":
                logger.debug(f'будет проведена повторная "authenticate"')
                string = user.action["authenticate"]
            elif logger.debug(f'начат обмен сообщениями msg, клиент пишет {user_action}'):
                user.action["msg"]["message"] = user_action
                logger.debug(f'подготовлена ветка для отправки {user.action["msg"]}')
                string = user.action["msg"]
                logger.debug(f'строка для отправки на сервер {string}')
            else:
                logger.debug(f'начат обмен в автоматическом режиме')
                user.action["msg"]["message"] = 'Проверка связи'
                logger.debug(f'строка для отправки на сервер {string}')
            data = json_dump_data(string)
            client_server_send(data)
            data = client_server_answer(BUFSIZE)
            data = json_load_data(data)
            print(data['alert'])



