"""
Задание 4.	Преобразовать слова «разработка», «администрирование»,
«protocol», «standard» из строкового представления в байтовое
и выполнить обратное преобразование (используя методы encode и decode).
"""
words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    w = word.encode('utf-8')
    print(w, type(w))
    w_b = bytes.decode(w, 'utf-8')
    print(w_b, type(w_b))
