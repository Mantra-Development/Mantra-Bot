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


@starboard_command.child
@lightbulb.command("toggle", "Toggle the starboard on and off")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toggle_command(ctx: lightbulb.Context) -> None:
    model = await StarConfig.get_or_none(guild_id=ctx.guild_id)
    if model is None:
        raise CommandError(
            "No starboard set for the channel\nUse `/starboard configure` to setup the channel first"
        )

    toggle = model.enabled
    model.enabled = not toggle
    await model.save()

    await ctx.respond(
        embed=hikari.Embed(
            description=f"{Emojis.STAR} Starboard has been {'disabled' if toggle else 'enabled'}!",
            color=Colors.ERROR if toggle else Colors.SUCCESS,
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@starboard.listener(hikari.GuildReactionAddEvent)
@starboard.listener(hikari.GuildReactionDeleteEvent)
async def starboard_handler(
    event: hikari.GuildReactionAddEvent | hikari.GuildReactionDeleteEvent,
) -> None:
    if not event.is_for_emoji("⭐"):
        return

    model = await StarConfig.get_or_none(guild_id=event.guild_id)
    if model is None:
        return

    if not model.channel_id or not model.enabled:
        return

    if model.channel_id == event.channel_id:
        return

    message = await event.app.rest.fetch_message(event.channel_id, event.message_id)
    reactions = [
        reaction for reaction in message.reactions if str(reaction.emoji) == "⭐"
    ]

    if not reactions:
        return

    stars = reactions[0].count

    if stars < model.star_count:
        return

    content, embed = starboard_embed_handler(message, stars)
    star_model = await StarboardEntries.get_or_none(
        guild_id=event.guild_id,
        message_id=event.message_id,
        channel_id=event.channel_id,
    )

    if star_model is None:
        starboard_message = await event.app.rest.create_message(
            model.channel_id, content=content or "", embed=embed
        )
        await StarboardEntries.create(
            guild_id=event.guild_id,
            channel_id=event.channel_id,
            message_id=event.message_id,
            starboard_message_id=starboard_message.id,
        )
        return

    starboard_id = star_model.starboard_message_id
    try:
        await event.app.rest.edit_message(
            channel=model.channel_id,
            message=star_model.starboard_message_id,
            content=content,
            embed=embed,
        )
    except hikari.NotFoundError:
        entries = await StarboardEntries.get_or_none(starboard_message_id=starboard_id)
        if entries is None:
            return
        await entries.delete()
        await starboard_handler(event)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(starboard)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(starboard)
