"""
Урок 2. Файловое хранение данных
Задание 1.
Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных
из файлов info_1.txt, info_2.txt, info_3.txt и формирующий
новый «отчетный» файл в формате CSV. Для этого:
a. Создать функцию get_data(), в которой в цикле осуществляется
    перебор файлов с данными, их открытие и считывание данных.
    В этой функции из считанных данных необходимо с помощью
    регулярных выражений извлечь значения параметров
    «Изготовитель системы»,  «Название ОС», «Код продукта»,
    «Тип системы». Значения каждого параметра поместить
    в соответствующий список. Должно получиться четыре списка —
    например, os_prod_list, os_name_list, os_code_list, os_type_list.
    В этой же функции создать главный список для хранения
    данных отчета — например, main_data — и поместить в
    него названия столбцов отчета в виде списка:
    «Изготовитель системы», «Название ОС», «Код продукта»,
    «Тип системы». Значения для этих столбцов также оформить
    в виде списка и поместить в файл main_data (также для каждого файла);
b. Создать функцию write_to_csv(), в которую передавать
    ссылку на CSV-файл. В этой функции реализовать получение
    данных через вызов функции get_data(), а также сохранение
    подготовленных данных в соответствующий CSV-файл;
c. Проверить работу программы через вызов функции write_to_csv().
"""
import csv
import re
from chardet import detect


def get_data(name_file):
    """
    :param name_file: Название файла, который следует обработать
    :return: Возвращается содержимое файла после проверки кодировки
    """
    with open(name_file, 'rb') as file:
        file_content = file.read()
        encoding = detect(file_content)['encoding']
        # print(encoding)
    with open(name_file, 'r', encoding=encoding) as file:
        values = file.readlines()
    return values


def regular_filter(item, string):
    """
    Функция получает строку поиска и строку где искать и в
    случае наличия строки поиска в строке где надо искать -
    возвращает остаток строки без лишних пробелов
    :param item: Строк которую ищем.
    :param string: Строка, в которой ищем.
    :return: Пустая строка или остаток строки без лишних пробелов
    """
    item = item
    # print(item)
    string = string
    # print(string)
    a = ''
    if item in string:
        string = string.replace(item,
                                '')
        a = re.sub(r'\s+', ' ', string)
    return a


def write_to_csv(data):
    """
    Функция получает данные и записывает их в файл main_data.csv
    :param data: Список для записи
    :return: Результатом является запись в файл
    """
    with open('main_data.csv', 'w') as f_n:
        f_n_writer = csv.writer(f_n)
        for row in data:
            f_n_writer.writerow(row)


"""

Начальные данные

"""

file_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
# список файлов, которые учавствуют в раздаче
os_prod_list = []   # список изготовителей
os_name_list = []   # список названий ОС
os_code_list = []   # список кодов продукта
os_type_list = []   # список типов системы
header = ['Изготовитель системы:', 'Название ОС:',
          'Код продукта:', 'Тип системы:']
list_attr = [header, os_code_list, os_name_list, os_prod_list, os_type_list]

# Перебор по списку фалов
for file_name in file_list:
    # Перебор по списку list_attr
    for j in range(0, 4):
        # Запрос содержимого файла
        frag = get_data(file_name)
        # Перебор по списку полей в файле
        for i in range(0, len(frag)):
            try:
                # Выделение остатка строки из сроки с записью
                content = regular_filter(item=header[j], string=frag[i])
                if content != '':
                    list_attr[j+1].append(content)
            except SyntaxError:
                print('')

print(list_attr)
# Сохранине данных в файл
write_to_csv(list_attr)
