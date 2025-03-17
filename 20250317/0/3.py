import asyncio


async def echo(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    while data := await reader.readline():
        match data.split():
            case [b"print", *tail]:
                writer.write(b" ".join(tail))
            case [b"info", b"host" | b"port" as info]:
                if info == b"host":
                    writer.write(me.split(":")[0].encode())
                else:
                    writer.write(me.split(":")[1].encode())
        writer.write(b"\n")
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
