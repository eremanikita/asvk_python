from enum import Enum
from cowsay import list_cows
import asyncio
import json


class Cows(Enum):
    JGSBAT = "jgsbat"


class Cord:
    def __init__(self, x=0, y=0):
        self.x: int = x
        self.y: int = y

    def to_dict(self):
        return {"x": self.x, "y": self.y}

    def __add__(self, other):
        return Cord((self.x + other.x) % 10, (self.y + other.y) % 10)

    def __str__(self):
        return f"({self.x}, {self.y})"


class Mob:
    def __init__(self, message, name, hp):
        self.message = message
        self.name = name
        self.hp = hp

    def get_damage(self, hp):
        damage_value = min(hp, self.hp)
        self.hp -= damage_value
        return self.hp, damage_value

    @staticmethod
    def check_name(name):
        return name in list_cows() or name in Cows


class Field:
    def __init__(self):
        self.field = [[None for _ in range(10)] for _ in range(10)]

    def add_mob(self, cord, name, message, hp):
        if Mob.check_name(name):
            self.field[cord.x][cord.y] = Mob(message, name, hp)
            return self.field[cord.x][cord.y]
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

    def move(self, direction: Cord):
        self.cord = self.cord + direction
        return self.cord


class GameSession:
    monsters = set()

    def __init__(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        self.field = Field()
        self.player = Player()

    def get_current_monster(self) -> Mob | None:
        return self.field.get_monster(self.player.cord)

    def get_monsters(self):
        return self.monsters

    def add_mob(self, cord: Cord, name: str, message: str, hp: int) -> bool:
        if answer := self.field.add_mob(cord, name, message, hp):
            self.monsters.add(answer)
            return True
        return False

    def encounter(self):
        if self.field.check_cell(self.player.cord):
            return self.field.get_monster(self.player.cord).name, self.field.get_monster(self.player.cord).message

    def move_player(self, direction: Cord):
        current_cord = self.player.move(direction)
        if response_monster := self.encounter():
            return {"coord": current_cord.to_dict(), "name": response_monster[0], "message": response_monster[1]}
        else:
            return {"coord": current_cord.to_dict()}

    def attack_monster(self, name: str, damage: int):
        if self.field.check_cell(self.player.cord) and (
                monster := self.field.get_monster(self.player.cord)).name == name:
            hp_value, damage_value = monster.get_damage(damage)
            if hp_value == 0:
                self.field.del_mob(self.player.cord)
                self.monsters.remove(monster)
            return hp_value, damage_value
        else:
            return None


async def echo(reader, writer):
    while data := await reader.readline():
        match (json_data := json.loads(data.decode()))['command']:
            case 'move':
                result = game.move_player(Cord(**json_data["params"]))
                writer.write(json.dumps(result).encode())
            case 'addmob':
                params = json_data["params"]
                result = game.add_mob(Cord(params["coords"]["x"], params["coords"]["y"]), params["name"],
                                      params["hello"], params["hp"])
                writer.write(json.dumps(result is not None).encode())
            case 'attack':
                params = json_data["params"]
                result = game.attack_monster(params["name"], params["hp"])
                writer.write(json.dumps(result).encode())
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


game = GameSession()
asyncio.run(main())
