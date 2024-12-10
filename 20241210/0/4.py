import asyncio


async def squarer(value):
    return value * value


async def doubler(value):
    return value + value


async def main(numbers):
    squared = await asyncio.gather(*(squarer(n) for n in numbers))
    doubled = await asyncio.gather(*(doubler(n) for n in squared))
    print(doubled)


asyncio.run(main([3, 5]))

