"""
Урок 2.
Задание 2.
Задание на закрепление знаний по модулю json.
Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается
5 параметров — товар (item), количество (quantity), цена (price),
покупатель (buyer), дата (date). Функция должна предусматривать
запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    """
    Функция обрабатывает и записывает параметры в файл
    json
    :param item:
    :param quantity:
    :param price:
    :param buyer:
    :param date:
    :return:
    """
    dict_to_json = {
        'товар': item,
        'количество': quantity,
        'цена': price,
        'покупатель': buyer,
        'дата': date
    }
    orders = {"orders": [
       dict_to_json
    ]}

    with open('orders.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(orders, ensure_ascii=False, indent=4))

# Входные данные


Data = ['Штаны', '10', 10.00, 'Филипов Антон', '15-04-2020 15:22']
Data2 = ['Пальто', '16', 11.00, 'Василь Быков', '17-04-2020 10:12']

write_order_to_json(Data[0], Data[1], Data[2], Data[3], Data[4])
write_order_to_json(Data2[0], Data2[1], Data2[2], Data2[3], Data2[4])
