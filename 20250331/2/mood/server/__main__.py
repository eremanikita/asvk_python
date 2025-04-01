import asyncio
from .server import Server

server = Server()
asyncio.run(server.run())
