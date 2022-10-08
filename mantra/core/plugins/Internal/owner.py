import logging
import re

import hikari
import lightbulb
import miru
import yuyo
from miru.ext import nav

from mantra.core.plugins.Internal import handle_plugins
from mantra.core.utils.errors import CommandError
from mantra.core.utils.eval_helpers import _yields_results, eval_python_code

owner = lightbulb.Plugin("Admin", "Administrator Commands Plugin")

logger = logging.getLogger(__name__)


@owner.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("shutdown", "Shutdown the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def shutdown_command(ctx: lightbulb.Context) -> None:
    logger.info("Shutting down the bot!")
    await ctx.respond(
        embed=hikari.Embed(
            description="Going back to sleep, See ya around!",
            color=0xFFA500,
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )
    await ctx.bot.close()


@owner.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option(
    "action",
    "Action to perform on the extension",
    choices=[
        "load",
        "unload",
        "reload",
    ],
)
@lightbulb.option("plugin", "The plugin to perform the action on")
@lightbulb.command(
    "extension", "Command Group related to reloading extensions", pass_options=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def extension_command(ctx: lightbulb.Context, action: str, plugin: str) -> None:
    if plugin == "mantra.core.plugins.Internal.owner":
        raise CommandError("Cannot perform actions on this plugin!")

    if action == "reload" and plugin == "all":
        ctx.bot.reload_extensions(*ctx.bot.extensions)
        return await ctx.respond(
            embed=hikari.Embed(description="Reloaded all extensions!", color=0x00FF00),
            flags=hikari.MessageFlag.EPHEMERAL,
        )

    await handle_plugins(ctx, plugin, action)


@owner.command
@lightbulb.command("eval", "Run Evals as Bot owner")
@lightbulb.implements(lightbulb.PrefixCommand)
async def eval_command(ctx: lightbulb.Context) -> None:
    assert ctx.event.message is not None
    code = re.findall(
        r"```(?:[\w]*\n?)([\s\S(^\\`{3})]*?)\n*```", ctx.event.message.content
    )
    if not code:
        raise CommandError("Expected a python code block.")
    stdout, stderr, exec_time, failed = await eval_python_code(ctx, code[0])
    color = 0xFF0000 if failed else 0x00FF00
    string_paginator = yuyo.sync_paginate_string(
        _yields_results(stdout, stderr), wrapper="```python\n{}\n```", char_limit=2034
    )
    fields = [
        hikari.Embed(
            color=color, description=text, title=f"Eval Page {page+1}"
        ).set_footer(text=f"Executed in: {exec_time}ms")
        for text, page in string_paginator
    ]

    navigator = nav.NavigatorView(
        pages=fields,
        buttons=[
            nav.PrevButton(),
            nav.StopButton(emoji="🗑️"),
            nav.NextButton(),
        ],
    )
    await navigator.send(ctx.channel_id)
    await navigator.wait()


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(owner)
    miru.load(bot)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(owner)
