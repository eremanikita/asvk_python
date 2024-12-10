import asyncio


async def squarer(value):
    return value * value


async def doubler(value):
    return value + value


async def main(numbers):
    async with asyncio.TaskGroup() as tg:
        squared_tasks = [tg.create_task(squarer(n)) for n in numbers]

    squared = [task.result() for task in squared_tasks]

    async with asyncio.TaskGroup() as tg:
        doubled_tasks = [tg.create_task(doubler(n)) for n in squared]

    doubled = [task.result() for task in doubled_tasks]

    print(doubled)


asyncio.run(main([3, 5]))

