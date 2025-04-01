import cmd
import json
import shlex
import readline
from cowsay import list_cows
from .models import Direction, Weapon, Cows
from .parser import ParserService


class MUDGame(cmd.Cmd):
    prompt = "command>> "

    def __init__(self, socket):
        super().__init__()
        self.s = socket

    def do_sayall(self, args):
        """Send other users a text message"""
        if args:
            self.s.sendall((json.dumps({"command": "sayall", "message": shlex.split(args)[0]}) + "\n").encode())

    def do_up(self, args):
        """Move the player up"""
        self.s.sendall((json.dumps({"command": "move", "params": Direction.UP.value.to_dict()}) + "\n").encode())

    def do_down(self, args):
        """Move the player down"""
        self.s.sendall((json.dumps({"command": "move", "params": Direction.DOWN.value.to_dict()}) + "\n").encode())

    def do_left(self, args):
        """Move the player left"""
        self.s.sendall((json.dumps({"command": "move", "params": Direction.LEFT.value.to_dict()}) + "\n").encode())

    def do_right(self, args):
        """Move the player right"""
        self.s.sendall((json.dumps({"command": "move", "params": Direction.RIGHT.value.to_dict()}) + "\n").encode())

    def do_addmob(self, args):
        """Add a mob to the field
        addmob <monster_name> hello <hello_string> hp <hitpoints> coords <x> <y>"""

        params = ParserService.parse_addmob(args)
        if params:
            self.s.sendall((json.dumps({"command": "addmob", "params": params}) + "\n").encode())
        else:
            print("Invalid command")

    def do_attack(self, args):
        """Attack the specific monster in the same cell if it is on it
        weapons:
            sword: -10 hp
            spear: -15 hp
            axe: -20 hp
        nothing if there is no monster in the same cell or the name is incorrect"""
        if (result := ParserService.parse_attack(args)) != -1:
            self.s.sendall(
                (json.dumps({"command": "attack", "params": {"name": result[0], "hp": result[1]}}) + "\n").encode())

    def complete_attack(self, text, line, begidx, endidx):
        parts = line.split(" ")
        if len(parts) == 2:
            return [c for c in list_cows() + Cows.custom_cows if c.startswith(text)]
        elif len(parts) == 3:
            return ["with"]
        elif len(parts) > 3 and parts[2] == "with":
            return [weapon.name.lower() for weapon in Weapon if weapon.name.lower().startswith(text)]
        return []

    def default(self, line):
        print("Invalid command")


def msg_reciever(cli, socket):
    while response := socket.recv(1024).rstrip().decode():
        last_command = readline.get_line_buffer() if (line := readline.get_line_buffer()) and line[-1] != "\n" else ""
        print(f"\n{response}\n{cli.prompt}{last_command}", end="", flush=True)
