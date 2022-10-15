import aiohttp
from pydantic import BaseModel

from mantra.core.utils.errors import CommandError


class Urban(BaseModel):
    definition: str
    permalink: str
    thumbs_up: str
    sound_urls: list
    author: str
    word: str
    defid: int
    current_vote: str
    written_on: str
    example: str
    thumbs_down: int


async def make_urban_request(term: str) -> list["Urban"]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.urbandictionary.com/v0/define?term={term}"
        ) as response:
            raw_data = await response.json()

            if not raw_data["list"]:
                raise CommandError(f"No results found for `{term}`")

    response_list = []
    for data in raw_data["list"]:
        response_list.append(Urban.construct(**data))

    return response_list
