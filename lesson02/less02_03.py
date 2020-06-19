"""
Урок 2.
3.Задание на закрепление знаний по модулю yaml.
Написать скрипт, автоматизирующий сохранение
данных в файле YAML-формата. Для этого:
a.Подготовить данные для записи в виде словаря, в котором первому
ключу соответствует список, второму — целое число, третьему —
вложенный словарь, где значение каждого ключа — это целое
число с юникод-символом, отсутствующим в кодировке ASCII (например, €);
b.Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность
работы с юникодом: allow_unicode = True;
c.Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
from ruamel import yaml

first, second, third, forth, fifth = 'first', 'second', 1, 'forth', 'fifth'
dict_to_yaml = {
    1: (first, second),
    2: third,
    3: {
        4: forth,
        5: fifth
    }

}
# запись тестового словаря в файл
with open('file.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(dict_to_yaml, f_n, default_flow_style=False)
# извлечение тестового словаря из файла и его вывод
with open('file.yaml', encoding='utf-8')as f_n:
    print(f_n.read())
