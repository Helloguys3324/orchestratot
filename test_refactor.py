import asyncio
from contextlib import contextmanager

@contextmanager
def handle():
    try:
        yield
    except Exception as e:
        print("Caught", e)

async def route1():
    with handle():
        await asyncio.sleep(0.1)
        raise ValueError("test")
        return "sync result"

async def main():
    await route1()

asyncio.run(main())
