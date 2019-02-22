import asyncio


def memoize(coro):
    cached_futures = {}

    async def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cached_futures:
            return await cached_futures[key]
        cached_futures[key] = asyncio.get_running_loop().create_future()
        result = await coro(*args, **kwargs)
        cached_futures[key].set_result(result)
        return result
    return wrapper
