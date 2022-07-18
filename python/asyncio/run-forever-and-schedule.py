import asyncio


async def coro1():
    print("in coro1")
    await asyncio.sleep(1)


async def coro2():
    print("in coro2")
    await asyncio.sleep(1)


def main():
    print("in main")
    asyncio.create_task(coro1())
    asyncio.create_task(coro2())


loop = asyncio.get_event_loop()
# loop.call_later takes only normal functions, not coros
# but it also takes `asyncio.create_task`
loop.call_later(1, main)
loop.run_forever()