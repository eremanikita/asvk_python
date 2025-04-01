from io import StringIO

import asyncio
import json
from cowsay import cowsay, read_dot_cow, list_cows


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
        return name in list_cows() or name in Cow.custom_cows


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
    users = dict()

    def __init__(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        self.field = Field()

    def get_current_monster(self, cord: Cord) -> Mob | None:
        return self.field.get_monster(cord)

    def get_monsters(self):
        return self.monsters

    def add_mob(self, cord: Cord, name: str, message: str, hp: int):
        if not (answer := self.field.add_mob(cord, name, message, hp)) is None:
            self.monsters.add(answer)
        return {"monster": answer, "coords": cord}

    def add_player(self, player_id):
        player = Player(player_id)
        self.users[player_id] = player

    def del_player(self, player_id):
        del self.users[player_id]

    def encounter(self, cord: Cord):
        if self.field.check_cell(cord):
            return self.field.get_monster(cord).name, self.field.get_monster(cord).message

    def move_player(self, player_id, direction: Cord):
        player = self.users[player_id]
        current_cord = player.move(direction)
        if response_monster := self.encounter(player.cord):
            return {"coords": current_cord.to_dict(), "name": response_monster[0], "message": response_monster[1]}
        else:
            return {"coords": current_cord.to_dict(), "name": None, "message": None}

    def attack_monster(self, player_id, name: str, damage: int):
        player = self.users[player_id]
        if self.field.check_cell(player.cord) and (monster := self.field.get_monster(player.cord)) and monster.name == name:
            hp_value, damage_value = monster.get_damage(damage)
            if hp_value == 0:
                self.field.del_mob(player.cord)
                self.monsters.remove(monster)
            return {"hp_remain": hp_value, "damage": damage_value, "name": name}
        else:
            return None


class UIResponse:

    @staticmethod
    def move_response(params):
        answer = ""
        answer += f"Moved to {Cord.from_dict(params["coords"])}\n"
        name, message = params["name"], params["message"]
        if name:
            if name in list_cows():
                return cowsay(message, cow=name)
            else:
                return cowsay(message, cowfile=read_dot_cow(StringIO(Cow.custom_cows[name])))
        return answer

    @staticmethod
    def addmob_response(params):
        monster, cord = params["monster"], params["coords"]
        if monster:
            return f"Added monster {monster.name} to {cord} saying {monster.message}\n"
        return "Cannot add unknown monster\n"

    @staticmethod
    def attack_response(params):
        if params:
            answer = f"Attacked {params["name"]}, damage {params["damage"]} hp\n"
            if params["hp_remain"] == 0:
                answer += f"{params["name"]} died\n"
            else:
                answer += f"{params["name"]} now has {params['hp_remain']}\n"
            return answer
        else:
            return "No monster here"


async def send_notifications(message, exception: str):
    for queue in users.keys():
        if queue != exception:
            await users[queue].put(message)


async def client_connection(reader, writer):
    player_id = "{}:{}".format(*writer.get_extra_info('peername'))
    queue = asyncio.Queue()
    username = None

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(queue.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for request in done:
            if request is send:
                send = asyncio.create_task(reader.readline())
                data = request.result()
                if not data:
                    break

                json_data = json.loads(data.decode())
                match json_data['command']:
                    case 'register':
                        username = json_data['username']
                        if username in users:
                            writer.write(f"0:username {username} exists.\n".encode())
                        else:
                            users[username] = queue
                            game.add_player(username)
                            writer.write(f"Hello, {username} in MUD game!\n".encode())
                            await send_notifications(f"{username} joined.\n", username)
                    case 'sayall':
                        await send_notifications(f"{username}: {json_data['message']}", username)
                    case 'move':
                        result = game.move_player(username, Cord(**json_data["params"]))
                        answer = UIResponse.move_response(result)
                        writer.write(answer.encode())
                    case 'addmob':
                        params = json_data["params"]
                        result = game.add_mob(Cord.from_dict(params["coords"]), params["name"], params["hello"],
                                              params["hp"])
                        answer = UIResponse.addmob_response(result)
                        writer.write(answer.encode())
                        if result["monster"]:
                            await send_notifications(f"{username} added {params["name"]} with {params["hp"]} hp.",
                                                     username)
                    case 'attack':
                        params = json_data["params"]
                        result = game.attack_monster(username, params["name"], params["hp"])
                        answer = UIResponse.attack_response(result)
                        writer.write(answer.encode())
                        if result:
                            notification = ""
                            notification += f"{username} attacked {params["name"]}. Damage {result["damage"]}.\n"
                            if result["hp_remain"] == 0:
                                notification += f"{result["name"]} died\n"
                            else:
                                notification += f"{result["name"]} now has {result['hp_remain']}.\n"
                            await send_notifications(notification, username)

            elif request is receive:
                receive = asyncio.create_task(queue.get())
                writer.write(f"{request.result()}\n".encode())
                await writer.drain()

    if username:
        game.del_player(username)
        users.pop(username)
        await send_notifications(f"{username} left", username)
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(client_connection, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


users = dict()
game = GameSession()
asyncio.run(main())
