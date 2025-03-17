import sys
import socket
import cmd
import readline


class client(cmd.Cmd):

    def do_print(self, args):
        s.sendall(f"print {args}\n".encode())
        print(s.recv(1024).rstrip().decode())

    def do_info(self, args):
        s.sendall(f"info {args}\n".encode())
        print(s.recv(1024).rstrip().decode())

    def complete_info(self, text, line, begidx, endidx):
        tokens = (line + '.').split()
        if len(tokens) == 2:
            return [i for i in ('host', 'port') if i.startswith(tokens[1][:-1])]


readline.parse_and_bind("bind ^I rl_complete")
host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    client().cmdloop()
