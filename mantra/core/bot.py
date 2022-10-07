import asyncio
import logging

import aiohttp
import hikari
import lightbulb
from tortoise import Tortoise

from mantra.config import bot_config

from .tortoise_config import tortoise_config

logger = logging.getLogger(__name__)


class Mantra(lightbulb.BotApp):
    def __init__(self) -> None:
        super().__init__(
            token=bot_config.token,
            default_enabled_guilds=bot_config.test_guilds,
            intents=hikari.Intents.ALL,
            help_slash_command=True,
            # cache_settings=CACHE_SETTINGS,
            ignore_bots=True,
        )

    def run_bot(self) -> None:
        self.event_manager.subscribe(hikari.StartingEvent, self.on_starting)
        self.event_manager.subscribe(hikari.StartedEvent, self.on_started)
        self.event_manager.subscribe(hikari.StoppingEvent, self.on_stopping)
        self.event_manager.subscribe(hikari.StoppedEvent, self.on_stopped)

        super().run(asyncio_debug=True)

    async def on_starting(self, event: hikari.StartingEvent) -> None:
        asyncio.create_task(self.establish_db_connection())
        self.load_extensions_from("./mantra/core/plugins", recursive=True)
        self.aiohttp_session = aiohttp.ClientSession()
        logger.info("Bot is starting!")

    async def on_started(self, event: hikari.StartedEvent) -> None:
        logger.info("Bot has started successfully!")

    async def on_stopping(self, event: hikari.StoppingEvent) -> None:
        await self.aiohttp_session.close()
        await Tortoise.close_connections()

    async def on_stopped(self, event: hikari.StoppedEvent) -> None:
        ...

    async def establish_db_connection(self) -> None:
        await Tortoise.init(tortoise_config)
