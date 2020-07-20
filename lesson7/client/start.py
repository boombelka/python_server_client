"""Запуск сервера и клиентских приложений."""

import subprocess

clients = []

while True:
    actions = input('1 - выход, '
                   '2 - начать работу клиентов '
                   '3 - окончание работы')

    if actions == '1':
        break
    elif actions == '2':

        clients.append(subprocess.Popen('python client.py -n test1',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        clients.append(subprocess.Popen('python client.py -n test2',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        clients.append(subprocess.Popen('python client.py -n test3',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif actions == '3':
        while clients:
            process = clients.pop()
            process.kill()
