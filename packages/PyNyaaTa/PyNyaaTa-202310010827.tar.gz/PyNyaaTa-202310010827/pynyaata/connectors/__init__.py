from asyncio import gather

from .animeultime import AnimeUltime
from .core import Other
from .nyaa import Nyaa


async def run_all(*args, **kwargs):
    coroutines = [Nyaa(*args, **kwargs).run(),
                  AnimeUltime(*args, **kwargs).run()]

    return list(await gather(*coroutines))


def get_instance(url, query=''):
    if 'nyaa.si' in url:
        return Nyaa(query)
    elif 'anime-ultime' in url:
        return AnimeUltime(query)
    else:
        return Other(query)
