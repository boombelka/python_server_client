"""
Задание 5.
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
 результаты из байтовового в строковый тип на кириллице.
"""
import subprocess

result_ping = [['ping', 'yandex.ru'], ['ping', 'yandex.com']]

for ping_n in result_ping:
    process_ping = subprocess.Popen(ping_n, stdout=subprocess.PIPE)
    i = 0
    for word in process_ping.stdout:
        if i < 10:
            print(word)
            word = word.decode('cp866').encode('utf-8')
            print(word.decode('utf-8'))
            i += 1
        else:
            print('конец пинга')
            break
