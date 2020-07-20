"""Клиентская часть приложения."""
from lesson03.client.cliconf import ADDR, BUFSIZE
from socket import AF_INET, SOCK_STREAM, socket
import json
from lesson03.client.user_client import User
import datetime
import logging
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
    logger.info(f'Преобразование строки данных для отправки на сервер.')
    data = json.dumps(string, ensure_ascii=False).encode('utf-8')
    return data


@log(logger=logging.getLogger('client'))
def json_load_data(b_data):
    logger.info(f'Преобразование результата ответа сервереа')
    data = json.loads(b_data, encoding="utf-8")
    return data


@log(logger=logging.getLogger('client'))
def client_server_answer(BUFSIZE):
    logger.info('Получение запроса клиента к серверу')
    server_answer = client_socket.recv(BUFSIZE).decode('utf-8')
    return server_answer


@log(logger=logging.getLogger('client'))
def client_server_send(data):
    logger.info('Отправление ответа сервера к клиенту')
    data = client_socket.send(data)
    return data


logger = logging.getLogger('client')

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
time_create = datetime.datetime.today().strftime("%d/%m/%y %H:%M:%S")

# при запуске клиента создается экземпляр
# класса пользователя, где хранятся
# необходимы реквизиты пользователя
user = User()
print(user.name)
logger.debug(f'создан пользователь с именем {user.name}.')
while True:
    if user.name == "noname":
        user.autenticate()
        string = user.action["authenticate"]
        # Импорт запроса в JSON строку.
        data = json_dump_data(string)

        client_socket.send(data)

        data = client_server_answer(BUFSIZE)

        data = json_load_data(data)

        user_set_change = user.set_change(data)
        logger.debug(f'Пользователь получил токен '
                     f'{user.token} и имя {user.name}')
    else:
        user_action = str(input('введите любое слово'))
        if user_action == "authenticate":
            logger.debug(f'будет проведена повторная "authenticate"')
            string = user.action["authenticate"]
        elif user_action == "msg":
            logger.debug(f'начат обмен сообщениями')
            string = user.action["msg"]
        else:
            logger.debug(f'начат обмен сообщениями msg, клиент пишет {user_action}')
            user.action["msg"]["message"] = user_action
            logger.debug(f'подготовлена ветка для отправки {user.action["msg"]}')
            string = user.action["msg"]
            logger.debug(f'строка для отправки на сервер {string}')
        data = json_dump_data(string)
        client_server_send(data)
        data = client_server_answer(BUFSIZE)
        data = json_load_data(data)

del user
client_socket.close()
logger.debug('соединение закрыто')
