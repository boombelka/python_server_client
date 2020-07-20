"""Словарь действий клиента."""
import datetime


"""Словарь действий action"""
action = {
    "presence": {"action": "presence",
                 "status": "False",
                 "info": "присутствие. Сервисное сообщение для "
                         "извещения сервера о присутствии клиента online",
                 },
    "prоbe": {"action": "prоbe",
              "status": "False",
              "info": "проверка присутствия. Сервисное сообщение "
                      "от сервера для проверки присутствии клиента online",
              },

    "msg": {"action": "msg",
            "message": "",
            "info": "простое сообщение пользователю или в чат",
            "token": "token"
            },
    "quit": {"action": "quit",
             "status": "False",
             "info": "отключение от сервера",
             },
    "authenticate": {
        "action": "authenticate",
        "time": "time",
        "user": {
                "account_name": "noname",
                "password": ""
            }
    }
}


if __name__ == '__main__':
    string = action
    print(string)
