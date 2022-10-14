import hikari
import lightbulb

from mantra.core.models import Guild
from mantra.core.utils import Colors, Emojis

admin = lightbulb.Plugin("Admin", "Admin Commands Plugin")
admin.add_checks(lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_GUILD))


@admin.command
@lightbulb.option("prefix", "Custom prefix for the server")
@lightbulb.command(
    "changeprefix", "Change custom prefix for the server", pass_options=True
)
@lightbulb.implements(lightbulb.SlashCommand)
async def change_prefix_command(ctx: lightbulb.Context, prefix: str) -> None:
    model = await Guild.get_or_none(id=ctx.guild_id)
    model.prefix = prefix
    await model.save()

    await ctx.respond(
        embed=hikari.Embed(
            description=f"{Emojis.SUCCESS} I set your server's prefix to `{prefix}`",
            color=Colors.SUCCESS,
        ),
        flags=hikari.MessageFlag.EPHEMERAL,
    )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(admin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(admin)
