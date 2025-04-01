import sys
import socket
import threading
import readline
import json
from .cli import MUDGame, msg_reciever

readline.parse_and_bind("bind ^I rl_complete")
host = "localhost"
port = 1337
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall((json.dumps({"command": "register", "username": sys.argv[1]}) + "\n").encode())
    response = s.recv(1024).rstrip().decode()
    if response[0] != '0':
        print(response)
        cli = MUDGame(s)
        request = threading.Thread(target=msg_reciever, args=(cli, s))
        request.start()
        cli.cmdloop()
    else:
        print(response[2:])
