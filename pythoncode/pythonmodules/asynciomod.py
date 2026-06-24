import asyncio


# async def main():
#     print('Hello ...')
#     await asyncio.sleep(1)
#     print('... World!')

# asyncio.run(main())

async def async_generator():
    tokens = ['Hello', 'World', 'from', 'async', 'generator!']
    for token in tokens:
        await  asyncio.sleep(1)
        yield token


async def main():
    async for token in async_generator():
        print(token, end=' ', flush=True)


if __name__ == '__main__':
    asyncio.run(main())



