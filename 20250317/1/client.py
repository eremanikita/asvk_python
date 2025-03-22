import readline
import cmd
import sys
import socket
from enum import Enum


class Direction(Enum):
    UP = "0 -1"
    DOWN = "0 1"
    RIGHT = "1 0"
    LEFT = "-1 0"


class Cord:
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class MUDGame(cmd.Cmd):
    prompt = "command>> "

    def do_up(self, args):
        """Move the player up"""
        s.sendall(f"move {Direction.UP}".encode())

    def do_down(self, args):
        """Move the player down"""
        s.sendall(f"move {Direction.DOWN}".encode())

    def do_left(self, args):
        """Move the player left"""
        s.sendall(f"move {Direction.LEFT}".encode())

    def do_right(self, args):
        """Move the player right"""
        s.sendall(f"move {Direction.RIGHT}".encode())

    def do_addmob(self, args):
        """Add a mob to the field
        addmob <monster_name> hello <hello_string> hp <hitpoints> coords <x> <y>"""
        pass

    def do_attack(self, args):
        """Attack the specific monster in the same cell if it is on it
        weapons:
            sword: -10 hp
            spear: -15 hp
            axe: -20 hp
        nothing if there is no monster in the same cell or the name is incorrect"""
        pass

    def default(self, line):
        print("Invalid command")


if __name__ == "__main__":
    readline.parse_and_bind("bind ^I rl_complete")
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        MUDGame().cmdloop()
