import math
import re

import hikari
import lightbulb

from mantra.core.utils import Colors, Emojis

errors = lightbulb.Plugin("Errors", "Error handling plugin for the bot")


@errors.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    error = event.exception

    if isinstance(error, lightbulb.CommandNotFound):
        return

    if isinstance(
        error,
        lightbulb.BotMissingRequiredPermission | lightbulb.MissingRequiredPermission,
    ):
        missing = [
            perm.replace("_", " ").replace("guild", "server").title()
            for perm in str(error.missing_perms).split("|")
        ]
        if len(missing) > 2:
            fmt = "{}, and {}".format("**, **".join(missing[:-1], missing[-1]))
        else:
            fmt = " and ".join(missing)
        symbol = (
            f"{Emojis.ERROR} I am"
            if isinstance(error, lightbulb.BotMissingRequiredPermission)
            else "You are"
        )
        description = (
            f"{symbol} missing the **{fmt}** permission(s) to run this command."
        )

        return await event.context.respond(
            flags=hikari.MessageFlag.EPHEMERAL,
            embed=hikari.Embed(
                title="Missing Required Permissions",
                color=Colors.ERROR,
                description=description,
            ),
        )

    if isinstance(error, lightbulb.CommandIsOnCooldown):
        return await event.context.respond(
            embed=hikari.Embed(
                title="Command on Cooldown",
                color=Colors.ALERT,
                description=f"{Emojis.WARNING} This command is on cooldown, try again after `{math.ceil(error.retry_after)}s`.",
            ),
            flags=hikari.MessageFlag.EPHEMERAL,
        )

    if isinstance(error, lightbulb.NotEnoughArguments):
        return await event.bot.help_command.send_command_help(
            event.context, event.context.command
        )

    title = " ".join(re.compile(r"[A-Z][a-z]*").findall(error.__class__.__name__))
    await event.context.respond(
        embed=hikari.Embed(
            title=f"{Emojis.ERROR} {title}", description=str(error), color=Colors.ERROR
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )
    raise error


def load(bot: lightbulb.BotApp):
    bot.add_plugin(errors)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(errors)
