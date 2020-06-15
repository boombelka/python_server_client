"""
Урок 1 Задание2.
Каждое из слов «class», «function», «method» записать в байтовом
типе без преобразования в последовательность кодов
(не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных.
"""

words_byte = [b'class', b'function', b'method']

for word_byte in words_byte:
    print('тип переменной : {}\n'.format(type(word_byte)), '  ',
          'содержание переменной : {}\n'.format(str(word_byte)), '  ',
          'длина строки : {}\n'.format(len(word_byte)))
