import json
import logging
import datetime
"""
Файл содержит процедуры для работы ответами сервера и
базой данных пользователей.
"""



def read_file_json():
    pass


def write_file_json(user):
    logger.debug(f'записы в файл {user}')
    with open("save.json", "w", encoding="utf-8") as write_file:
        json.dump(user, write_file, ensure_ascii=False)


def save_user(user_attr):
    """
    Функция формирует файл базы данных пользователей.
    :param user_attr: входят 2 компонента логин/пароль tuple.
    :return: ответ сервера.
    """
    # Проверка отсутствия файла базы данных пользователей.
    # В случае отсуствия файла базы данных пользователей,
    # создается пустой файл.
    try:
        with open("save.json", "r", encoding="utf-8")as read_file:
            read_file.read()
    except FileNotFoundError:
        with open("save.json", "w", encoding="utf-8")as write_file:
            write_file.write("")
    # Попытка десериализовать прочитанную строку
    try:
        with open("save.json", "r", encoding="utf-8")as read_file:
            _ = dict(json.loads(read_file.read()))
    except json.decoder.JSONDecodeError:
        # Проверка на некорректную при которой декодировать запись невозможно
        # В случае невозможности прочитать запись - файл перезаписывается
        # целиком
        user = {"user0": {"account_name": user_attr[0], "password": user_attr[1]}}
        write_file_json(user)

    except TypeError:
        # Проверка на некорректную запись в списке пользователей
        # В случае невозможности прочитать запись - файл перезаписывается
        # целиком
        user = {"user0": {"account_name": user_attr[0], "password": user_attr[1]}}
        write_file_json(user)

    # Попытка прочитать перезаписанный файл. В случае
    # успешной попытки производится поиск пары логин/пароль
    # и установление флага регистрация или нет.
    # Отказ авторизации осущетсвляется только в
    # случае наличия логина в базе с неверным паролем.
    with open("save.json", "r", encoding="utf-8") as read_file:
        list_users = json.loads(read_file.read())
    if len(list_users) > 0:
        for number in range(0, len(list_users)):
            user_number = str("user" + str(number))
            # проверка на совпадение логина и пароля с базой,
            # да - зарегистрирован
            if user_number in list_users:
                if list_users[user_number]["account_name"] == str(user_attr[0]) \
                        and list_users[user_number]["password"] == str(user_attr[1]):
                    answer = 200
                    logger.debug(f'Пользователь: {user_attr[0]}/{user_attr[1]} присутствует в базе'
                                 f'Ответ сервера {answer}')
                    return answer

                elif list_users[user_number]["account_name"] == str(user_attr[0]) and list_users[user_number]["password"] != str(user_attr[1]):
                    answer = 402
                    logger.debug(f'Неверный пароль')

                    return answer
        # проверка на не совпадение логина и пароля - новый пользователь
        # в этом случае данные заносятся в базу данных
        user = {str("user" + str(len(list_users) + 1)): {"account_name": user_attr[0], "password": user_attr[1]}}
        list_users.update(user)
        write_file_json(list_users)
        answer = 201
        logger.debug(f'Пользователь: {user_attr[0]}/{user_attr[1]} отсутствует в базе.'
                     f'Добавлена новая учетная запись пользователя')
        return answer

    else:
        answer = 400
    logger.debug(f'ответ сервера {answer}')
    return answer


logger = logging.getLogger('server')

# Словарь действий action
action = {
    "presence": {True, "присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online"},
    "prоbe": {True, "проверка присутствия. Сервисное сообщение от сервера для проверки присутствии клиента online"},
    "msg": {"msg": "простое сообщение пользователю или в чат",
            "token": "token"},
    "quit": {"alert": "отключение от сервера",
             "token": "token"},
    "authenticate": {
        "action": "authenticate",
        "status": "no_authenticate",
        "module": "save_user",
        "time": datetime.datetime.today().strftime("%d/%m/%y %H:%M:%S"),
            "user": {
                    "account_name": "noname",
                    "password": "None"
            }
    }
}

server_answer = {
    "200": {
        "response": 200,
        "alert": "Необязательное сообщение/уведомление",
        "token": "asd",
    },
    "201": {
        "response": 201,
        "alert": "Создана новая учетная запись",
        "token": "abd",
    },
    "402": {
        "response": 402,
        "alert": "Неверная пара логин/пароль",
        "token": "abd",
    },
    "400": {
        "response": 400,
        "alert": "Ваш запрос не принят к сведению",
        "token": "abd",
    }
}


if __name__ == '__main__':
    print(server_answer["200"])


