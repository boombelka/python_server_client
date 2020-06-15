"""
Задание 3.	Определить, какие из слов «attribute», «класс», «функция»,
 «type» невозможно записать в байтовом типе.
"""

word1 = 'attribute'
word2 = b'класс'
word3 = b'функция'
word4 = b'type'

# На строке word2 = b'класс' написанный на кирилице выходит ошибка
# SyntaxError: bytes can only contain ASCII literal characters.
# т.к. ASCII не поддерживает килилицу
