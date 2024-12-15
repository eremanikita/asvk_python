import asyncio

stop_event = asyncio.Event()


async def writer(queue, delay):
    count = 0
    while not stop_event.is_set():
        await asyncio.sleep(delay)
        await queue.put(f"{count}_{delay}")
        count += 1


async def stacker(queue, stack):
    while not stop_event.is_set():
        stack.append(await queue.get())


async def reader(stack, number, delay):
    for i in range(number):
        while not stack:
            await asyncio.sleep(0)
        print(stack.pop())
        await asyncio.sleep(delay)
    stop_event.set()


async def main():
    delay1, delay2, delay3, number = eval(input())
    queue = asyncio.Queue()
    stack = []

    tasks = [
        asyncio.create_task(writer(queue, delay1)),
        asyncio.create_task(writer(queue, delay2)),
        asyncio.create_task(stacker(queue, stack)),
        asyncio.create_task(reader(stack, number, delay3))
    ]

    await asyncio.gather(*tasks)


asyncio.run(main())

