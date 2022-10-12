import aiohttp


class Animals(object):
    def __init__(self, image: str, fact: str):
        self.image = image
        self.fact = fact


async def make_request(type: str) -> "Animals":
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://some-random-api.ml/animal/{type}") as response:
            data = await response.json()

    return Animals(**data)
