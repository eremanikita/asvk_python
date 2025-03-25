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

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

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
        return name in list_cows() or any(cow.name == name for cow in Cows)


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
    def __init__(self, player_id):
        self.id = player_id
        self.cord = Cord()

    def move(self, direction: Cord):
        self.cord = self.cord + direction
        return self.cord


class GameSession:
    monsters = set()
    players = dict()

    def __init__(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        self.field = Field()

    def get_current_monster(self, cord: Cord) -> Mob | None:
        return self.field.get_monster(cord)

    def get_monsters(self):
        return self.monsters

    def get_players(self):
        return self.players.keys()

    def add_mob(self, cord: Cord, name: str, message: str, hp: int) -> bool:
        if not (answer := self.field.add_mob(cord, name, message, hp)) is None:
            self.monsters.add(answer)
            return True
        return False

    def add_player(self, player_id):
        player = Player(player_id)
        self.players[player_id] = player

    def del_player(self, player_id):
        del self.players[player_id]

    def encounter(self, cord: Cord):
        if self.field.check_cell(cord):
            return self.field.get_monster(cord).name, self.field.get_monster(cord).message

    def move_player(self, player_id, direction: Cord):
        player = self.players[player_id]
        current_cord = player.move(direction)
        if response_monster := self.encounter(player.cord):
            return {"coord": current_cord.to_dict(), "name": response_monster[0], "message": response_monster[1]}
        else:
            return {"coord": current_cord.to_dict()}

    def attack_monster(self, player_id, name: str, damage: int):
        player = self.players[player_id]
        if self.field.check_cell(player) and (
                monster := self.field.get_monster(player)).name == name:
            hp_value, damage_value = monster.get_damage(damage)
            if hp_value == 0:
                self.field.del_mob(player)
                self.monsters.remove(monster)
            return hp_value, damage_value
        else:
            return None


async def send_notifications(message, exception: str):
    for queue in clients.keys():
        if queue != exception:
            await clients[queue].put(message)


async def client_connection(reader, writer):
    player_id = "{}:{}".format(*writer.get_extra_info('peername'))
    game.add_player(player_id)
    await send_notifications(f"Player {player_id} joined", player_id)
    queue = asyncio.Queue()
    clients[player_id] = queue

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())
    while True:
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if task is send:
                send = asyncio.create_task(reader.readline())
                data = task.result()
                if not data:
                    game.del_player(player_id)
                    await send_notifications(f"Player {player_id} has left", player_id)
                    return
                json_data = json.loads(data.decode())

                match json_data['command']:
                    case 'move':
                        result = game.move_player(player_id, Cord(**json_data["params"]))
                        await queue.put(json.dumps(result))
                    case 'addmob':
                        params = json_data["params"]
                        result = game.add_mob(Cord.from_dict(params["coords"]), params["name"], params["hello"],
                                              params["hp"])
                        await queue.put(json.dumps(result))
                    case 'attack':
                        params = json_data["params"]
                        result = game.attack_monster(player_id, params["name"], params["hp"])
                        await queue.put(json.dumps(result))

            elif task is receive:
                receive = asyncio.create_task(queue.get())
                writer.write(f"{task.result()}\n".encode())
                await writer.drain()


async def main():
    server = await asyncio.start_server(client_connection, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


clients = dict()
game = GameSession()
asyncio.run(main())
