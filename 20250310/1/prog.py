import cmd
import readline
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


class Cord:
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return f"({self.x}, {self.y})"


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

    def get_damage(self, hp):
        damage_value = min(hp, self.hp)
        self.hp -= damage_value
        return self.hp, damage_value

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
            return self.field[cord.x][cord.y]
        else:
            print("Cannot add unknown monster")
            return None

    def get_monster(self, cord) -> Mob | None:
        return self.field[cord.x][cord.y]

    def del_mob(self, cord):
        self.field[cord.x][cord.y] = None

    def check_cell(self, cord: Cord):
        return not self.get_monster(cord) is None


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
    DAMAGE_FACTOR = 10
    monsters = set()

    def __init__(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        self.field = Field()
        self.player = Player()

    def get_current_monster(self) -> Mob | None:
        return self.field.get_monster(self.player.cord)

    def get_monsters(self):
        return self.monsters

    def add_mob(self, cord: Cord, name: str, message: str, hp: int) -> None:
        if answer := self.field.add_mob(cord, name, message, hp):
            self.monsters.add(answer)

    def encounter(self):
        if self.field.check_cell(self.player.cord):
            self.field.get_monster(self.player.cord).say()

    def move_player(self, direction: Direction):
        self.player.move(direction)
        self.encounter()

    def attack_monster(self):
        if self.field.check_cell(self.player.cord):
            monster = self.field.get_monster(self.player.cord)
            hp_value, damage_value = monster.get_damage(GameSession.DAMAGE_FACTOR)
            print(f"Attacked {monster.name}, damage {damage_value} hp")
            if hp_value == 0:
                print(f"{monster.name} died")
                self.field.del_mob(self.player.cord)
                self.monsters.remove(monster)
            else:
                print(f"{monster.name} now has {hp_value}")
        else:
            print("No monster here")


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
                    params["coords"] = Cord(int(tokens[i + 1]), int(tokens[i + 2]))
                i += 3
            else:
                i += 1

        return params if not (ParserService.required_keys - params.keys()) else None

    @staticmethod
    def parse_attack(line, monster: Mob | None) -> bool:
        tokens = shlex.split(line)
        if len(tokens) != 1:
            print("Invalid command")
        elif monster and tokens[0] == monster.name:
            return True
        else:
            print(f"No {tokens[0]} here")
        return False



class MUDGame(cmd.Cmd):
    game = GameSession()
    AVAILABLE_MONSTER_NAMES = list_cows() | Cow.custom_cows.keys()
    prompt = "command>> "

    def do_up(self, args):
        """Move the player up"""
        self.game.move_player(Direction.UP)

    def do_down(self, args):
        """Move the player down"""
        self.game.move_player(Direction.DOWN)

    def do_left(self, args):
        """Move the player left"""
        self.game.move_player(Direction.LEFT)

    def do_right(self, args):
        """Move the player right"""
        MUDGame.game.move_player(Direction.RIGHT)

    def do_addmob(self, args):
        """Add a mob to the field
        addmob <monster_name> hello <hello_string> hp <hitpoints> coords <x> <y>"""
        params = ParserService.parse_addmob(args)
        if params:
            MUDGame.game.add_mob(params["coords"], params["name"], params["hello"], params["hp"])
        else:
            print("Invalid command")

    def do_attack(self, args):
        """Attack the specific monster in the same cell if it is on it
        -10 hp
        nothing if there is no monster in the same cell or the name is incorrect"""
        if ParserService.parse_attack(args, MUDGame.game.get_current_monster()):
            MUDGame.game.attack_monster()

    def complete_attack(self, text, line, begidx, endidx):
        parts = line.split(" ")
        if len(parts) == 2:
            return [c for c in self.AVAILABLE_MONSTER_NAMES if c.startswith(text)]

    def default(self, line):
        print("Invalid command")


if __name__ == "__main__":
    readline.parse_and_bind("bind ^I rl_complete")
    MUDGame().cmdloop()
