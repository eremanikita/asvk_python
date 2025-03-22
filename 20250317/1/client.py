import readline
import cmd
import sys
import socket
import shlex
from enum import Enum
import json
from io import StringIO

from cowsay import list_cows, cowsay, read_dot_cow


class Cow:
    custom_cows = {
        "jgsbat": """    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\\\--//|.'-._  (
     )'   .'\\/o\\/o\\/'.   `(
      ) .' . \\====/ . '. (
       )  / <<    >> \\  (
        '-._/``  ``\\_.-'
  jgs     __\\\\'--'//__
         (((""`  `"")))"""
    }


class Cord:
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def to_dict(self):
        return {"x": self.x, "y": self.y}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Direction(Enum):
    UP = Cord(0, -1)
    DOWN = Cord(0, 1)
    RIGHT = Cord(1, 0)
    LEFT = Cord(-1, 0)


class Weapon(Enum):
    SWORD = 10
    SPEAR = 15
    AXE = 20


class ParserService:
    required_keys = {"name", "hello", "hp", "coords"}

    @staticmethod
    def parse_addmob(line: str):
        tokens = shlex.split(line)
        params = {"name": tokens[0]}
        i = 1
        token_length = len(tokens)
        while i < token_length:
            if tokens[i] == "hello":
                if i + 1 < token_length:
                    params["hello"] = tokens[i + 1]
                i += 2
            elif tokens[i] == "hp":
                if i + 1 < len(tokens) and tokens[i + 1].isdigit() and int(tokens[i + 1]) > 0:
                    params["hp"] = int(tokens[i + 1])
                i += 2
            elif tokens[i] == "coords":
                if i + 2 < len(tokens) and tokens[i + 1].isdigit() and tokens[i + 2].isdigit():
                    params["coords"] = Cord(int(tokens[i + 1]), int(tokens[i + 2])).to_dict()
                i += 3
            else:
                i += 1

        return params if not (ParserService.required_keys - params.keys()) else None

    @staticmethod
    def parse_attack(line):
        tokens = shlex.split(line)
        if len(tokens) == 0:
            print("Invalid command")
        else:
            if len(tokens) == 3 and tokens[1] == "with":
                weapon_name = tokens[2].upper()
            else:
                weapon_name = Weapon.SWORD.name

            if any(weapon_name == i.name for i in Weapon):
                return tokens[0], Weapon[weapon_name].value
            else:
                print("Unknown weapon")
        return -1


class UIService:
    @staticmethod
    def print_player_move(response):
        print(f"Moved to {Cord.from_dict(response["coord"])}")
        if "name" in response:
            name, message = response["name"], response["message"]
            if name in list_cows():
                print(cowsay(message, cow=name))
            else:
                print(cowsay(message, cowfile=read_dot_cow(StringIO(Cow.custom_cows[name]))))

    @staticmethod
    def print_addmob(response, name, coords, message):
        if response:
            print(
                f"Added monster {name} to {Cord.from_dict(coords)} saying {message}")
        else:
            print("Cannot add unknown monster")

    @staticmethod
    def print_attack(response, name):
        if response:
            print(f"Attacked {name}, damage {response[1]} hp")
            if response[0] == 0:
                print(f"{name} died")
            else:
                print(f"{name} now has {response[0]}")
        else:
            print("No monster here")


class MUDGame(cmd.Cmd):
    prompt = "command>> "

    def do_up(self, args):
        """Move the player up"""
        s.sendall((json.dumps({"command": "move", "params": Direction.UP.value.to_dict()}) + "\n").encode())
        response = json.loads(s.recv(1024).decode())
        UIService.print_player_move(response)

    def do_down(self, args):
        """Move the player down"""
        s.sendall((json.dumps({"command": "move", "params": Direction.DOWN.value.to_dict()}) + "\n").encode())
        response = json.loads(s.recv(1024).decode())
        UIService.print_player_move(response)

    def do_left(self, args):
        """Move the player left"""
        s.sendall((json.dumps({"command": "move", "params": Direction.LEFT.value.to_dict()}) + "\n").encode())
        response = json.loads(s.recv(1024).decode())
        UIService.print_player_move(response)

    def do_right(self, args):
        """Move the player right"""
        s.sendall((json.dumps({"command": "move", "params": Direction.RIGHT.value.to_dict()}) + "\n").encode())
        response = json.loads(s.recv(1024).decode())
        UIService.print_player_move(response)

    def do_addmob(self, args):
        """Add a mob to the field
        addmob <monster_name> hello <hello_string> hp <hitpoints> coords <x> <y>"""

        params = ParserService.parse_addmob(args)
        if params:
            s.sendall((json.dumps({"command": "addmob", "params": params}) + "\n").encode())
            response = json.loads(s.recv(1024).decode())
            UIService.print_addmob(response, params["name"], params["coords"], params["hello"])
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
            s.sendall(
                (json.dumps({"command": "attack", "params": {"name": result[0], "hp": result[1]}}) + "\n").encode())
            response = json.loads(s.recv(1024).decode())
            UIService.print_attack(response, result[0])

    def complete_attack(self, text, line, begidx, endidx):
        parts = line.split(" ")
        if len(parts) == 2:
            return [c for c in list_cows() if c.startswith(text)]
        elif len(parts) == 3:
            return ["with"]
        elif len(parts) > 3 and parts[2] == "with":
            return [weapon.name.lower() for weapon in Weapon if weapon.name.lower().startswith(text)]
        return []

    def default(self, line):
        print("Invalid command")


if __name__ == "__main__":
    readline.parse_and_bind("bind ^I rl_complete")
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        s.connect((host, port))
        MUDGame().cmdloop()
