import hikari
import lightbulb

from mantra.core.utils import CommandError


async def handle_plugins(ctx: lightbulb.Context, plugin: str, action: str) -> None:
    try:
        getattr(ctx.bot, f"{action}_extensions")(plugin)
    except lightbulb.ExtensionAlreadyLoaded:
        raise CommandError(f"Plugin `{plugin}` is already loaded.")
    except lightbulb.ExtensionNotLoaded:
        raise CommandError(f"Plugin `{plugin}` doesn't seem to be loaded")

    await ctx.respond(
        embed=hikari.Embed(
            description=f"`{plugin}` {action}ed successfully!", color=0x00FF00
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )
