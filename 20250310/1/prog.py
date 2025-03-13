import cmd

from enum import Enum
from cowsay import cowsay, list_cows, read_dot_cow
from io import StringIO
import shlex


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


class Direction(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class Mob:
    def __init__(self, message, name, hp):
        self.message = message
        self.name = name
        self.hp = hp

    def say(self):
        if self.name in list_cows():
            print(cowsay(self.message, cow=self.name))
        else:
            print(cowsay(self.message, cowfile=read_dot_cow(StringIO(Cow.custom_cows[self.name]))))

    @staticmethod
    def check_name(name):
        return name in list_cows() or name in Cow.custom_cows


class Field:
    def __init__(self):
        self.field = [[None for _ in range(10)] for _ in range(10)]

    def add_mob(self, cord, name, message, hp):
        if Mob.check_name(name):
            self.field[cord.x][cord.y] = Mob(message, name, hp)
            print(f"Added monster {name} to ({cord.x}, {cord.y}) saying {message}")
        else:
            print("Cannot add unknown monster")


class Cord:
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"({self.x}, {self.y})"


class Player:
    def __init__(self):
        self.cord = Cord()

    def move(self, direction: Direction):
        match direction:
            case Direction.UP:
                self.cord = Cord(self.cord.x, (self.cord.y - 1) % 10)
            case Direction.DOWN:
                self.cord = Cord(self.cord.x, (self.cord.y + 1) % 10)
            case Direction.LEFT:
                self.cord = Cord((self.cord.x - 1) % 10, self.cord.y)
            case Direction.RIGHT:
                self.cord = Cord((self.cord.x + 1) % 10, self.cord.y)
        print(f"Moved to {self.cord}")


class GameSession:
    def __init__(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        self.field = Field()
        self.player = Player()

    def add_mob(self, cord: Cord, name: str, message: str, hp: int) -> None:
        self.field.add_mob(cord, name, message, hp)

    def encounter(self):
        if self.field.field[self.player.cord.x][self.player.cord.y] is not None:
            self.field.field[self.player.cord.x][self.player.cord.y].say()

    def move_player(self, direction: Direction):
        self.player.move(direction)
        self.encounter()


class MUDGame(cmd.Cmd):
    game = GameSession()
    prompt = "command>> "

    def do_up(self, args):
        self.game.move_player(Direction.UP)

    def do_down(self, args):
        self.game.move_player(Direction.DOWN)

    def do_left(self, args):
        self.game.move_player(Direction.LEFT)

    def do_right(self, args):
        self.game.move_player(Direction.RIGHT)

    def do_addmob(self, args):
        pass

    def default(self, line):
        print("Invalid command")


if __name__ == "__main__":
    MUDGame().cmdloop()
