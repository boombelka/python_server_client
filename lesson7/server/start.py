"""Запуск сервера."""

import subprocess

clients = []

while True:
    actions = input('1 - выход, '
                   '2 - начать работу '
                   '3 - окончание работы')

    if actions == '1':
        break
    elif actions == '2':
        clients.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif actions == '3':
        while clients:
            process = clients.pop()
            process.kill()