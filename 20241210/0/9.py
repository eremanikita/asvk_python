import asyncio


async def prod(q1):
    for i in range(5):
        value = f"value_{i}"
        await q1.put(value)
        print(f"prod: put {value} to q1")
        await asyncio.sleep(1)
    print("prod: finished producing")


async def mid(q1, q2):
    while True:
        value = await q1.get()
        print(f"mid: got {value} from q1")
        await q2.put(value)
        print(f"mid: put {value} to q2")


async def cons(q2):
    while True:
        value = await q2.get()
        print(f"cons: got {value} from q2")


async def main():
    q1 = asyncio.Queue()
    q2 = asyncio.Queue()

    ptask = asyncio.create_task(prod(q1))
    mtask = asyncio.create_task(mid(q1, q2))
    ctask = asyncio.create_task(cons(q2))

    await ptask


asyncio.run(main())

