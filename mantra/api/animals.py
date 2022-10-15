import aiohttp
from pydantic import BaseModel


class Animals(BaseModel):
    image: str
    fact: str


async def make_request(type: str) -> "Animals":
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://some-random-api.ml/animal/{type}") as response:
            data = await response.json()

    return Animals.construct(**data)
