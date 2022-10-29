from datetime import datetime

import hikari
import lightbulb

from mantra.core.models import StarboardEntries, StarConfig
from mantra.core.utils import Colors, CommandError, Emojis

from . import starboard_embed_handler

starboard = lightbulb.Plugin("Starboard", "Plugin containing starboard commands")


@starboard.command
@lightbulb.command("starboard", "Starboard command group")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def starboard_command(_: lightbulb.Context) -> None:
    ...


@starboard_command.child
@lightbulb.option(
    "channel",
    "The channel to set as starboard channel",
    type=hikari.GuildChannel,
    channel_types=hikari.ChannelType.GUILD_TEXT,
)
@lightbulb.option("threshold", "The star threshold for the server", type=int)
@lightbulb.command("configure", "Configure starboard for the server", pass_options=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def configure_command(
    ctx: lightbulb.Context, channel: hikari.GuildTextChannel, threshold: int
) -> None:
    model = await StarConfig.get_or_none(guild_id=ctx.guild_id)
    if model is None:
        await StarConfig.create(
            guild_id=ctx.guild_id, channel_id=channel.id, star_count=threshold
        )
    else:
        model.channel_id = channel.id
        model.star_count = threshold
        await model.save()

    await ctx.respond(
        embed=hikari.Embed(
            color=Colors.SUCCESS,
            description=f"{Emojis.SUCCESS} Starboard configured successfully!\n\n**Channel**: <#{channel.id}>\n**Threshold:** {threshold}",
            timestamp=datetime.now().astimezone(),
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(starboard)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(starboard)
