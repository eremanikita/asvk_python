"""Main server python file to start the server."""
import asyncio
from .server import Server

server = Server()
asyncio.run(server.run())
