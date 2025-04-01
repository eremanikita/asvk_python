import asyncio
import json
from .session import GameSession
from .models import Cord
from .ui import send_notifications, UIResponse


class Server:

    def __init__(self, host='0.0.0.0', port=1337):
        self.host = host
        self.port = port
        self.users = dict()
        self.game = GameSession()

    async def handle_connection(self, reader, writer):
        player_id = "{}:{}".format(*writer.get_extra_info('peername'))
        print(f"{player_id} connected")
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
                            if username in self.users:
                                writer.write(f"0:username {username} exists.\n".encode())
                                return
                            else:
                                self.users[username] = queue
                                self.game.add_player(username)
                                print(self.users)
                                writer.write(f"Hello, {username} in MUD game!\n".encode())
                                await send_notifications(self.users, f"{username} joined.\n", username)
                        case 'sayall':
                            await send_notifications(self.users, f"{username}: {json_data['message']}", username)
                        case 'move':
                            result = self.game.move_player(username, Cord(**json_data["params"]))
                            answer = UIResponse.move_response(result)
                            writer.write(answer.encode())
                        case 'addmob':
                            params = json_data["params"]
                            result = self.game.add_mob(Cord.from_dict(params["coords"]), params["name"],
                                                       params["hello"],
                                                       params["hp"])
                            answer = UIResponse.addmob_response(result)
                            writer.write(answer.encode())
                            if result["monster"]:
                                await send_notifications(self.users,
                                                         f"{username} added {params["name"]} with {params["hp"]} hp.",
                                                         username)
                        case 'attack':
                            params = json_data["params"]
                            result = self.game.attack_monster(username, params["name"], params["hp"])
                            answer = UIResponse.attack_response(result)
                            writer.write(answer.encode())
                            if result:
                                notification = ""
                                notification += f"{username} attacked {params["name"]}. Damage {result["damage"]}.\n"
                                if result["hp_remain"] == 0:
                                    notification += f"{result["name"]} died\n"
                                else:
                                    notification += f"{result["name"]} now has {result['hp_remain']}.\n"
                                await send_notifications(self.users, notification, username)

                elif request is receive:
                    receive = asyncio.create_task(queue.get())
                    writer.write(f"{request.result()}\n".encode())
                    await writer.drain()

        if username:
            self.game.del_player(username)
            self.users.pop(username)
            await send_notifications(self.users, f"{username} left", username)
        writer.close()
        await writer.wait_closed()

    async def run(self):
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        async with server:
            await server.serve_forever()
