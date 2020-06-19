"""
    Задача 6.
    6.	Создать текстовый файл test_file.txt, заполнить его тремя строками:
    «сетевое программирование», «сокет», «декоратор».
    Проверить кодировку файла по умолчанию.
    Принудительно открыть файл в формате Unicode и вывести его содержимое.
"""
import locale

string_word = ['сетевое программирование', 'сокет', 'декоратор']

# создание файла
with open('results.txt', 'w+') as file:
    for word in string_word:
        file.write(word + '\n')
    file.seek(0)

print(file)  # распечатка содержимого файла

print(file)

file_code = locale.getpreferredencoding()

# Чтение из файла
with open('results.txt', 'r', encoding=file_code) as file:
    for word in file:
        print(word)
    file.seek(0)
