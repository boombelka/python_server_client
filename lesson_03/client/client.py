"""
Клиентская часть приложения.
"""
from lesson03.client.cliconf import ADDR, BUFSIZE
from socket import AF_INET, SOCK_STREAM, socket
import json
from lesson03.client.users.user_client import User
import datetime
import logging
import lesson_03.client.client_log_config
# не разобрался - убираешь - не работает


logger = logging.getLogger('client')

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
time_create = datetime.datetime.today().strftime("%d/%m/%y %H:%M:%S")

# при запуске клиента создается экземпляр
# класса пользователя, где хранятся
# необходимы реквизиты пользователя
user = User(time_create)
logger.debug(f'создан пользователь с именем {user.name}')
while True:
    if user.name == "noname":
        user.autenticate()
        string = user.action["authenticate"]
        logger.debug(f'Создана строка для запроса авторизации на сервере: '
                     f'{string}')
        data = json.dumps(string, ensure_ascii=False)
        logger.debug(f'Создание соединения: {time_create}')
        data = data.encode('utf-8')
        client_socket.send(data)
        logger.debug(f'Создание соединения: отправлены данные на сервер {data}')
        data = client_socket.recv(BUFSIZE)
        data = data.decode('utf-8')
        logger.debug(f'Создание соединения: получены данные {data}')
        data = json.loads(data, encoding="utf-8")
        logger.debug(f'данные переведены из json {data}')
        user_set_change = user.set_change(data)
        logger.debug(f'Пользователь получил токен {user.token}')
    else:
        user_action = str(input('введите любое слово'))
        if user_action == "authenticate":
            logger.debug(f'будет проведена повторная "authenticate"')
            string = user.action["authenticate"]
        elif user_action == "msg":
            logger.debug(f'начат обмен сообщениями')
            string = user.action["msg"]
        else:
            logger.debug(f'начат обмен сообщениями')
            string = user.action["msg"]
        data = json.dumps(string, ensure_ascii=False)
        client_socket.send(data.encode('utf-8'))
        data = client_socket.recv(BUFSIZE)
        data = json.loads(data.decode('utf-8'), encoding="utf-8")
    input('Введите слово')
del user
client_socket.close()
logger.debug('соединение закрыто')
