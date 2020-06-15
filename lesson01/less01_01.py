"""
Урок 1 задание 1
1. Каждое из слов «разработка», «сокет», «декоратор»
представить в строковом формате и проверить тип и содержание
соответствующих переменных. Затем с помощью онлайн-конвертера
преобразовать строковые представление в формат
Unicode и также проверить тип и содержимое переменных.
"""
word1 = 'разработка'
word2 = 'сокет'
word3 = 'декоратор'
words = [word1, word2, word3]
# Данные полученные из конвертера
words_converter = [
                    b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0',
                    b'\xd1\x81\xd0\xbe\xd0\xba\xd0\xb5\xd1\x82',
                    b'\xd0\xb4\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80'
                    ]
for word in words:
    print('тип переменной : {}\n'.format(type(word)), '  ',
          'содержание переменной : {}\n'.format(str(word)), '  ',
          'длина строки : {}\n'.format(len(word)))

for word in words_converter:
    print('тип переменной : {}\n'.format(type(word)), '  ',
          'содержание переменной : {}\n'.format(str(word)), '  ',
          'длина строки : {}\n'.format(len(word)))
