from datetime import datetime, timedelta
from typing import TYPE_CHECKING, cast

import hikari
import lightbulb

from mantra.core.utils import Emojis, time_converter

from . import send_remainder

if TYPE_CHECKING:
    from mantra.core.bot import Mantra

utils = lightbulb.Plugin("Info", "Plugin that contains all the utility commands")


@utils.command
@lightbulb.add_cooldown(1, 5, lightbulb.UserBucket)
@lightbulb.option(
    "remainder", "Message for the remainder", modifier=lightbulb.OptionModifier.GREEDY
)
@lightbulb.option("time", "Time period for the remainder")
@lightbulb.command("remind", "Create a remainder", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def remainder_command(ctx: lightbulb.Context, time: str, remainder: str) -> None:
    bot = cast("Mantra", ctx.app)
    seconds = time_converter(time)
    bot.scheduler.add_job(
        send_remainder,
        "date",
        (ctx, remainder),
        next_run_time=datetime.now() + timedelta(seconds=int(seconds)),
    )

    await ctx.respond(
        f"Created a remainder for you! {Emojis.SUCCESS}",
        flags=hikari.MessageFlag.EPHEMERAL,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(utils)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(utils)
