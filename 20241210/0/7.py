import asyncio


async def snd(event):
    print(f"snd: generated {event}")
    event.set()


async def mid(k, event, event_id):
    await event.wait()
    print(f"mid({k}): received evsnd")
    print(f"mid({k}): generated evmid{event_id}")
    event_id[k].set()


async def rcv(event_id):
    await event_id[0].wait()
    print("rcv: received evmid0")
    await event_id[1].wait()
    print("rcv: received evmid1")


async def main():
    event = asyncio.Event()
    event_id = [asyncio.Event() for i in range(2)]

    await asyncio.gather(
        rcv(event_id),
        mid(1, event, event_id),
        mid(0, event, event_id),
        snd(event),
    )


asyncio.run(main())

